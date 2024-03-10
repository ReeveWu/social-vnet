import os
import dotenv
from langchain_openai import ChatOpenAI
from langchain.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate

dotenv.load_dotenv()

neo4j_url = os.getenv("NEO4J_CONNECTION_URL")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model_name="gpt-4-1106-preview")

cypher_generation_template = """
You are an expert Neo4j Cypher translator who converts English to Cypher based on the Neo4j Schema provided, following the instructions below:
1. Generate Cypher query compatible ONLY for Neo4j Version 5.
2. Do not use EXISTS, SIZE, HAVING keywords in the cypher. Use alias when using the WITH keyword.
3. Use only Nodes and relationships mentioned in the schema.
4. Always do a case-insensitive and fuzzy search for any properties related search. For example, to search for a Movie, use `toLower(movie.title) contains 'matrix'`. To search for a Director, use 'toLower(director.name) contains 'nolan'`. To search for a Genre, use `toLower(genre.name) contains 'action'`.
5. Never use relationships that are not mentioned in the given schema.
6. When asked about movies, match the properties using case-insensitive matching and the OR-operator, e.g., to find an action movie, use `toLower(movie.description) contains 'action' OR toLower(genre.name) contains 'action'`.
7. Whenever querying for information about movies, strive to include related information beyond the Movie node itself, such as Director and Genre, to provide a richer context. Use multiple MATCH statements or OPTIONAL MATCH to ensure related nodes are included in the results, even if some relationships are missing for certain movies.
8. For string matching, don't using SQL-like syntax; instead, use Cypher's pattern matching and string functions such as CONTAINS, STARTS WITH, ENDS WITH, and =~ for regular expression matching.

schema: {schema}

Examples:
Question: Tell me three movies in the action genre?
Answer: ```MATCH (m:Movie)-[:HAS_GENRE]->(g:Genre)
WHERE toLower(m.title) IS NOT NULL AND toLower(g.name) =~ '.*action.*'
RETURN m.title
ORDER BY rand()
LIMIT 3```
Question: List me the movies directed by D. J. Caruso. 
Answer: ```MATCH (m:Movie)-[:DIRECTED_BY]->(d:Director)
WHERE toLower(d.name) =~ '.*d\\. j\\. caruso.*'
RETURN m.title```

NOTE: 
DO NOT use EXISTS(), SIZE(), HAVING() keywords in the cypher.

Question: {question}
Only output the Cypher query.
"""

cypher_prompt = PromptTemplate(
    template = cypher_generation_template,
    input_variables = ["question", "schema"]
)

CYPHER_QA_TEMPLATE = """You are an assistant that helps to form nice and human understandable answers.
The information part contains the provided information that you must use to construct an answer.
The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
If the provided information is empty, say that you don't know the answer.
Final answer should be easily readable and structured.
Information:
{context}

Question: {question}
Helpful Answer:"""

qa_prompt = PromptTemplate(
    input_variables=["context", "question"], template=CYPHER_QA_TEMPLATE
)

def query_graph(user_input):
    graph = Neo4jGraph(url=neo4j_url, username=neo4j_user, password=neo4j_password)
    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=True,
        return_intermediate_steps=True,
        cypher_prompt=cypher_prompt,
        qa_prompt=qa_prompt
        )
    chain.cypher_generation_chain.prompt.input_variables = ["question", "schema"]
    result = chain(user_input)
    return result['result'], result['intermediate_steps'][0]['query'], result['intermediate_steps'][1]['context']
