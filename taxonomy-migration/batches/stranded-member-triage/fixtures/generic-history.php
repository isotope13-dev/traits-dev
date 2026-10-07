<?php
array_unshift($_SESSION['history'], $command);
if (preg_match('/^[[:blank:]]*cd[[:blank:]]*$/', $command)) { echo "history"; }
?>
<script>command_hist[current_line] = document.shell.command.value;
if (e.keyCode == 38 && current_line < command_hist.length-1) { current_line--; }</script>
