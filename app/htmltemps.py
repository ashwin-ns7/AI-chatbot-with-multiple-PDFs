css = '''
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.chat-message {
    display: flex;
    align-items: flex-start;
    max-width: 80%;
    border-radius: 20px;
    padding: 1rem;
    margin: 0.5rem;
    color: white;
    word-wrap: break-word;
}

.chat-message.user {
    background-color: #2b313e;
    align-self: flex-start;
    border-bottom-left-radius: 0;
}

.chat-message.bot {
    background-color: #475063;
    align-self: flex-end;
    border-bottom-right-radius: 0;
}

.chat-message .avatar {
    width: 40px;
    height: 40px;
    margin-right: 1rem;
    border-radius: 50%;
    overflow: hidden;
}

.chat-message.bot .avatar {
    margin-left: 1rem;
    margin-right: 0;
}

.chat-message img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.chat-message .message {
    flex: 1;
}
</style>
'''

bot_template = '''
<div class="chat-container">
    <div class="chat-message bot">
        <div class="message">{{MSG}}</div>
        <div class="avatar">
            <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" alt="Bot">
        </div>
    </div>
</div>
'''

user_template = '''
<div class="chat-container">
    <div class="chat-message user">
        <div class="avatar">
            <img src="https://cdn-icons-png.flaticon.com/512/4712/4712040.png" alt="User">
        </div>
        <div class="message">{{MSG}}</div>
    </div>
</div>
'''
