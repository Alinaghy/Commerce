document.addEventListener('DOMContentLoaded', function() {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);
    
    // By default, load the inbox
    load_mailbox('inbox');
    
    document.querySelector('#sub').addEventListener('click', function(){
        const x = document.querySelector('#compose-recipients').value;
        const y = document.querySelector('#compose-subject').value;
        var z = document.querySelector('#compose-body').value;
        
        fetch('/emails', {
            method: 'POST',
            body: JSON.stringify({
                    
                recipients: x,
                subject:  y,
                body: z
            })
        })
        .then(response =>response.json())
        .then(result => {
            if (result.E){
                document.querySelector('#error').innerHTML = `* ${result.E}`;
            }
            if(result.S){
                window.location.reload();
            }
        
        });
        
    
    
        
    });
    //--------------------------
    
    
    
    });
    
    
    
    document.addEventListener('click', event => {
    
        const element = event.target;
        if (element.className === 'post'){
            view_email(element.id);
        }
    
        if (element.className === 'archive'){
    
            element.parentElement.style.animationPlayState = 'running';
            element.parentNode.addEventListener('animationend',()=>{
            fetch(`/emails/${element.id}`, {
            method: 'PUT',
            body: JSON.stringify({
            archived: true
            })
            })
            .then(element.parentElement.remove());
    
            });
        
        }
        if (element.className === 'unarchive'){
    
            element.parentElement.style.animationPlayState = 'running';
            element.parentNode.addEventListener('animationend',()=>{
            fetch(`/emails/${element.id}`, {
            method: 'PUT',
            body: JSON.stringify({
            archived: false
            })
            })
            .then(element.parentElement.remove())
            .then(window.location.reload());
            });
            
        }
    
        if (element.className === 'reply'){
            var rec = document.querySelector('#sender').textContent;
            var sub = document.querySelector('#subject').textContent;
            var bod = document.querySelector('#body').textContent;
            var time = document.querySelector('.time').textContent;
            reply_email(rec,sub,bod,time);
        }
    
    });
    
    
    function compose_email() {
    
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
    }
    
    
    function reply_email(reci,subj,body,timest) {
    
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = `${reci}`;
    document.querySelector('#compose-body').innerHTML= `On ${timest}
    <${reci}> wrote :  ${body}`;
    let text = `${subj}`;
    if (text.includes("Re:")){
        document.querySelector('#compose-subject').value = `${subj}`;
    } else {
        document.querySelector('#compose-subject').value = `Re: ${subj}`;
    }
    
    }
    
    //load mailbox
    function load_mailbox(mailbox) {
    
    // Show the mailbox and hide other views
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#emails-view').style.display = 'block';
    
    
    // show emails
    fetch(`/emails/${mailbox}`)
    .then(response=>response.json())
    .then(emails=>{
    document.querySelector('#emails-view').innerHTML = "";
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    emails.forEach(add_inbox);
    
    
    });
    }
    
    //add inbox function
    function add_inbox(contents){
    const post = document.createElement('div');
    post.className = 'post';
    post.id = contents.id;
    post.innerHTML =   `<b><p id="sender1">${contents.sender}</p></b> <p id="subject1">${contents.subject}</p> <p id="timestamp1">${contents.timestamp}</p> <button class="archive" id="${contents.id}">Archive</button> <button class="unarchive" id="${contents.id}">Unarchive</button>`;
    
    if (contents.read == false){
        post.style.backgroundColor = "white";
    }
    else{
        post.style.backgroundColor = "#a8acaf";
    }
    
    var mailb = document.querySelector('h3').textContent;
    if (mailb === 'Sent'){
        post.querySelector('.archive').style.display = 'none';
        post.querySelector('.unarchive').style.display = 'none';
    }
    if (mailb === 'Archive'){
        post.querySelector('.archive').style.display = 'none';
        post.querySelector('.unarchive').style.display = 'inline-flex';
        
        
    }
    if (mailb === 'Inbox'){
        post.querySelector('.archive').style.display = 'inline-flex';
        post.querySelector('.unarchive').style.display = 'none';
    }
    
    document.querySelector('#emails-view').append(post);
    
    }
    
    
    //view email function
    function view_email(id){
    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
    document.querySelector('#emails-view').innerHTML = "";
    document.querySelector('#emails-view').innerHTML =   `<div class="as"><b id="bform">Form: </b> <p id="sender"> ${email.sender}</p></div>  <p id="recipiens"><b>To:</b> ${email.recipients}</p>   <div class="as"><b>Subject:</b><p id="subject"> ${email.subject}</p></div><br>  <div class="as"><b>Timestamp:</b><p class="time"> ${email.timestamp}</p></div><br> <button class="reply">Reply</button> <hr> <p id="body">${email.body}</p> `;
    
    });
    
    fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
    read: true
    })
    })
    
    }
    