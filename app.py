from flask import Flask, request, jsonify
import json
from datetime import datetime
from backend.ai_engine import ai_respond

app = Flask(__name__)

with open("data/businesses.json") as f:
    BUSINESSES = json.load(f)["businesses"]

with open("data/leads.json") as f:
    LEADS = json.load(f)["leads"]

with open("data/conversations.json") as f:
    CONVERSATIONS = json.load(f)["conversations"]

def save_db():
    with open("data/leads.json","w") as f:
        json.dump({"leads":LEADS},f,indent=4)
    with open("data/conversations.json","w") as f:
        json.dump({"conversations":CONVERSATIONS},f,indent=4)

@app.route("/start_conversation",methods=["POST"])
def start_conversation():
    data=request.json
    business_id=data["business_id"]
    lead_info=data["lead_info"]
    business=next(b for b in BUSINESSES if b["business_id"]==business_id)
    
    lead_id=f"lead{len(LEADS)+1:03d}"
    lead_info["lead_id"]=lead_id
    lead_info["business_id"]=business_id
    lead_info["conversation_status"]="active"
    lead_info["appointment_booked"]=False
    lead_info["last_message_time"]=datetime.now().isoformat()
    LEADS.append(lead_info)
    
    conv_id=f"conv{len(CONVERSATIONS)+1:03d}"
    CONVERSATIONS.append({"conversation_id":conv_id,
                          "lead_id":lead_id,
                          "messages":[],
                          "detected_objections":[],
                          "last_action":None})
    save_db()
    response,_=ai_respond(business,lead_info,conv_id,"")
    return jsonify({"conversation_id":conv_id,"response":response})

@app.route("/send_message",methods=["POST"])
def send_message():
    data=request.json
    conv_id=data["conversation_id"]
    user_message=data["message"]
    
    conv=next(c for c in CONVERSATIONS if c["conversation_id"]==conv_id)
    lead=next(l for l in LEADS if l["lead_id"]==conv["lead_id"])
    business=next(b for b in BUSINESSES if b["business_id"]==lead["business_id"])
    
    response,updated=ai_respond(business,lead,conv_id,user_message)
    for k,v in updated.items():
        if v: lead[k]=v
    conv["messages"].append({"text":user_message,"sender":"lead","timestamp":datetime.now().isoformat()})
    conv["messages"].append({"text":response,"sender":"AI","timestamp":datetime.now().isoformat()})
    lead["last_message_time"]=datetime.now().isoformat()
    save_db()
    return jsonify({"response":response})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=3000)
