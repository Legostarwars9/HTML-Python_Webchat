# HTML-Python_Webchat
<h2>So I was once looking for a Web Based Application like Discord that I could set up in my home on a Raspberry PI mini server that I have. I couldn't find one that I could easily install onto my Raspberry PI and set up within a few minutes...</h2>

<h2>So with help of ChatGPT, I created one.</h2>

<h2>--Features--</h2>
<ul>
  <h3>Chatting (Duh)</h3>
  <h3>Simple Moderation Control</h3>
  <ul>
    <h4>Commands (/delete, /ban, /mute, /ip-ban, /unmute, etc)</h4>
    <h4>Quick Delete Mode</h4>
  </ul>
</ul>

<h2>-Planned Features-</h2>
<ul>
  <h3>File Sharing</h3>
  <h3>Image Imbeding</h3>
</ul>

<h1>Bugs</h1>
<h2>-Stable Bugs-</h2>
<ul>
    <h3>Muting users does not work properly</h3>
    <h3>Banning users does not work properly</h3>
</ul>
<h2>-Experimental Bugs-</h2>
<ul>
    <h3>Commands Do not work properly</h3>
    <h3>Admin UI does not load</h3>
</ul>

<h1>Usage</h1>
<h2>How to use</h2>
<h3>
  1. Download Latest Release
  2. Run chat.py
  3. Go to localhost:5000
  4. Done
</h3>

<h2>
  -Commands List-
</h2>
<ul>
  <h3>/delete - Deletes a message - Syntax: /delete [Message ID]</h3>
  <h3>/mute - temporarily mutes a user until unmuted or server restarts - Syntax: /mute [Username] (Muting and Unmuting does not currently work</h3>
  <h3>/unmute - unmutes a user - Syntax: /unmute [Username]</h3>
  <h3>/ban - Bans a user - Syntax: /ban [Username] (Currently does not work)</h3>
  <h3>/unban - Unbans a user - Syntax: /unban [Username]</h3>
  <h3>/ip-ban - Bans a IP address - /ip-ban [Username] (only in experimental build)</h3>
</ul>
