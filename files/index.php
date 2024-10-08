<?php 
$files = glob('*');

foreach($files as $file) {
if($file != 'index.php'){
  echo           "<a href='/files/".$file."'>'" .  $file . "</a><br>";
}
}