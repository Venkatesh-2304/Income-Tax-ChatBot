import asyncio
from ai4 import translate
import openai
import os 
os.environ["OPENAI_API_KEY"] = openai.api_key = "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"

from paperqa import Docs

from langchain.chat_models import ChatAnthropic, ChatOpenAI
from paperqa import PromptCollection,prompts
from langchain.prompts import PromptTemplate as LangChainPromptTemplate
from haystack.nodes.prompt import PromptTemplate as haystackPromptTemplate

from haystack.nodes import OpenAIAnswerGenerator
from haystack.nodes import EmbeddingRetriever
from haystack.document_stores import InMemoryDocumentStore
import pickle 

###Retrive Document Store ### 
it_rules_docs = pickle.load( open("it_rules_docs.pkl" , "rb") )
it_faq_docs = pickle.load( open("it_faq_docs.pkl" , "rb"))

model = ChatOpenAI(model='gpt-3.5-turbo')
it_rules_docs.llm = model

it_faq_retriver = EmbeddingRetriever(
               document_store=it_faq_docs,
               embedding_model="text-embedding-ada-002",
               batch_size = 10,
               api_key="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",
               max_seq_len = 10000
)
###

###Intialize Prompts & Generators### 
faq_prompt = haystackPromptTemplate(name="en_qa",prompt_text="""
         You are  agent to help answer people queries about income tax rules in india .Answer the Question based on the below context, under 2 sentence .If the answer is not present in the context , extract it from internet .  
         ###
         Question : {query} 
         ### 
         Context :  {context}
         ### 
         Answer  :
         """)
faq_generator = OpenAIAnswerGenerator(api_key="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", 
                                         model="text-davinci-003", temperature=0.1,max_tokens=2000,
                                         prompt_template=faq_prompt )
####
my_qaprompt = LangChainPromptTemplate(
    input_variables=["context", "question"],
    template="You need to help users asnwer queries regarding income tax . "
    " Answer the question '{question}' unser 3 sentences and give the sections which could be referred for further reading"
    "Use the context below to answer the question . The context is rules  regarding income tax ."
    "If there is insufficient context, use the internet to retrive  answers. "
    "Context: {context}\n\n")

rules_prompts=PromptCollection(qa=my_qaprompt)
it_rules_docs.prompts = rules_prompts
###

#Functions 

def question_translate(q,lang="hi"):
    return translate(lang,"en",q)

def answer_simplifier(ans) : 
    rephrased_ans = openai.Completion.create(
         model="text-davinci-003",
         prompt=f"""Rephrase the below sentence without changing the meaning , strictly use only the vocabulary that is understandable for a 10 year old . 
                    ###
                    Sentence : {ans}
                 """,
         temperature=0.2,
         max_tokens=500,
         top_p=1.0,
         frequency_penalty=0.0,
         presence_penalty=0.0
       )
    rephrased_ans =rephrased_ans["choices"][0]["text"].strip()
    rephrased_ans = rephrased_ans.replace("%"," percentage")
    return rephrased_ans
    
def answer_translate(ans,lang="hi") : 
    return translate("en",lang,ans)

def answer_it_faq(q) :    
    docs = it_faq_retriver.run_query(q,top_k=3,)
    ans = faq_generator.run( q , documents= docs[0]['documents'] , top_k= 1 )[0]["answers"][0].answer
    return ans 

def answer_it_rules(q) : 
    res  = it_rules_docs.query(q, k = 5 , max_sources=3 , 
                        marginal_relevance=False)
    return res.answer 
  



