<?php

session_start();

// The amount of money you currently have on your account
$account = $_SESSION['you']['amount'];
// The amount of money you want to pay
$amount = (int)$_GET['amount'];
if ($amount < 0) { exit("No stealing plz"); }

// Perform payment, but only if you have enough money for it
if ($account - $amount >= 0) {
	// Add payment to authorized payments
	$id = bin2hex(random_bytes(10));
	$_SESSION['payments'][$id] = $amount;
	header("Refresh: 3;url=finalize_payment.php?id=$id");
	echo "Payment authorized with ID $id.<br/>Processing payment authorization...";
} else {
	echo "Payment authorization failed. Not enough money.";
}

//Idea: fare scambio di account dopo l'autorizzazione del pagamento
//main account session_id = a93bf6bc2e74fc2be85d5219a5bb9723
