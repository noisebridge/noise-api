<html>
<head><title>Noisebridge Gate</title></head>
<style>
label {
display: block;
}
div.box {
max-width: 500px;
margin: 1%;
border: 1px solid #3b6e22;
padding: 1% 1%;
}
</style>
<body>
<script>
function keycode_shortcut() {
    keycode_form = document.getElementById('keycodeform');
    keycode_value = document.getElementById('keycodevalue').value;
    keycode_form.setAttribute('action', "key/" + keycode_value);
}
</script>
<h1>Noisebridge Gate</h1>
<p>
<div class="box">
<h2>Open the door</h2>
<form action="." method="post">
<label for="key">Keycode:</label>
<input type="password" id="key" name="key" required="true" autofocus="autofocus">
<input type="hidden" name="open" value="true"><br>
<input type="submit" value="Open Door">
</form>
</div>

<div class="box">
<h2>Get a new keycode for a friend</h2>
<form id="keycodeform" action="key/" method="post">
<label for="keycodevalue">Your keycode:</label>
<input type="password" id="keycodevalue" name="keycode" required=true><br>
<label for="prefered">The keycode your friend would like, if any:</label>
<input type="text" id="preferred" name="preferred"><br>
<input type="hidden" name="create" value="true">
<label for="comment">Their name or nym, and email address (required):</label>
<input type="text" id="comment" name="comment" required=true placeholder="name, email address"><br>
<p>Remember: You are responsible for your new friend. If they are creepy or beat up robots or steal stuff, your keycode may be revoked as well as theirs.</p>
<input type="submit" value="Get a new keycode" onclick="keycode_shortcut()">
</form>
</div>
</body>
</html>
