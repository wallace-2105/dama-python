<?php
// Zera o placar, salvando uma lista vazia no arquivo
$arquivoPlacar = __DIR__ . '/placar.json';
file_put_contents($arquivoPlacar, json_encode([]));

// Volta pra página principal
header('Location: index.php');
exit;
