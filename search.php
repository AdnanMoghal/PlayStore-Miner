<?php

$query = escapeshellcmd($_POST['search']);

echo $query;

shell_exec('scrapy crawl playstore_levels -a search_term='.$query);

header('Location: ../files');
die();