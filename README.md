# HTML-Python_Webchat
<h3>So I was once looking for a Web Based Application like Discord that I could set up in my home on a Raspberry PI mini server that I have. I couldn't find one that I could easily install onto my Raspberry PI and set up within a few minutes...</h3>

<h3>So with help of ChatGPT, I created one.</h3>

<h2>--Features--</h2>
<ul>
  <h4>Chatting (Duh)</h4>
  <h4>Simple Moderation Control</h4>
  <ul>
    <h5>Commands (/delete, /ban, /mute, /ip-ban, /unmute, etc)</h5>
    <h5>Quick Delete Mode</h5>
  </ul>
</ul>

<h2>-Planned Features-</h2>
<ul>
  <h4>File Sharing</h4>
  <h4>Image Imbeding</h4>
</ul>

<h1>Bugs</h1>
<h2>-Stable Bugs-</h2>
<ul>
    <h4>Muting users does not work properly</h4>
    <h4>Banning users does not work properly</h4>
    <h4></h4>
</ul>
<h2>-Experimental Bugs-</h2>
<ul>
    <h4>Commands Do not work properly</h3>
    <h4>Admin UI does not load</h3>
</ul>

<h1>Usage</h1>
<h2>How to use</h2>
<h4>
  1. Download Latest Release <br>
  2. Run chat.py <br> 
  3. Go to localhost:5000 <br>
  4. Done <br>
</h4>

<h2>How to host to the internet</h2>
<h4>
  1. Start chat.py<br>
  2. Port forward port 5000 on your router<br>
  3. go to [Your IP]:5000<br>
</h4>

<h2>How to host behind CGNAT</h2>
<h4>
  1. Install your favorite reverse proxy (ngrok, playit.gg premium, Cloudflare, etc) <br>
  2. Start chat.py <br>
  3. Start the reverse proxy provider of your choice on port 5000<br>
  4. Go to the IP it gives you OR your custom domain you set up with the proivider.<br><br>
  -Example commmands with Cloudflared free url<br>
    [User]/chat> python3 chat.py<br>
    [User]/chat> cloudflared --url localhost:5000<br>
</h4>

<h2>How to get Admin</h2>
<h4>
  1. Have some access to the device the server is hosted on<br>
  2. Navigate to Users.txt<br>
  3. Find your User<br>
  4. Change [Username]:[Encryped Password]:user > [Username]:[Encryped Password]:admin<br>
  5. Log out and log back in <br>
</h4>

<h2>Commands List</h2>
<ul>
  <h3>/delete - Deletes a message - Syntax: /delete [Message ID]</h3>
  <h3>/mute - temporarily mutes a user until unmuted or server restarts - Syntax: /mute [Username] (Muting and Unmuting does not currently work</h3>
  <h3>/unmute - unmutes a user - Syntax: /unmute [Username]</h3>
  <h3>/ban - Bans a user - Syntax: /ban [Username] (Currently does not work)</h3>
  <h3>/unban - Unbans a user - Syntax: /unban [Username]</h3>
  <h3>/ip-ban - Bans a IP address - /ip-ban [Username] (only in experimental build)</h3>
</ul>
