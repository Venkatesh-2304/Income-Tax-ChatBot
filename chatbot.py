from chat_functions import * 
import pprint 

def chatbot(q,q_lang,a_lang,is_simplify,model) : 
      q_en = question_translate(q,q_lang)
      
      if model == "income_tax_rules" : 
         a_en = answer_it_rules(q_en)
      elif model == "income_tax_faq" :       
         a_en = answer_it_faq(q_en)
      else : raise Exception("Chatbot Model Not found")

      if is_simplify : 
         a_en = answer_simplifier(a_en)

      answer = answer_translate(a_en,a_lang)
      return { "q_en" : q_en , "a_en" : a_en , "answer" : answer  }
      

q = "मैं गृह ऋण ब्याज का भुगतान करने के लिए कितना कटौती कर सकता हूं?"
q_lang = a_lang = "hi"
is_simplify = True 
model = "income_tax_faq" #"income_tax_rules"
print("ChatBot Intiated...")
response = chatbot(q,q_lang,a_lang,is_simplify,model)
pprint.pprint( response )

     

    
