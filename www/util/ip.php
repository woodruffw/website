<?php

# filter_var shouldn't be necessary, but do it anyways
print filter_var($_SERVER['REMOTE_ADDR'], FILTER_VALIDATE_IP);

?>
