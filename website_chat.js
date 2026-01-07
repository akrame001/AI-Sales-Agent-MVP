let currentConvId="";

function showButtons(options,cb){
  const d=document.getElementById("buttons");
  d.innerHTML="";
  options.forEach(o=>{
    const btn=document.createElement("button");
    btn.innerText=o;
    btn.onclick=()=>cb(o);
    d.appendChild(btn);
  });
}

function sendMsg(msg){
  fetch("/send_message",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({conversation_id:currentConvId,message:msg})
  })
  .then(r=>r.json())
  .then(d=>{
    showMsg("AI:"+d.response);
  });
}

function showMsg(txt){
  const p=document.createElement("p");
  p.innerText=txt;
  document.getElementById("chatbox").appendChild(p);
}
