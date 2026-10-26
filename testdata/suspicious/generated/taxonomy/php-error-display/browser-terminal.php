<?php ?>
<script>
fetch(document.location.href + '?terminal=1', {
  method: 'POST', body: JSON.stringify({cmd: command})
});
</script>
