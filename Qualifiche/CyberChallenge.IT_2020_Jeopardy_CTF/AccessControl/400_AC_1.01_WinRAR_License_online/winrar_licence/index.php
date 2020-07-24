<?php

session_start();

include 'includes/header.php';

if (isset($_SESSION['you']) && isset($_SESSION['winrar'])) {
	echo "<div class='col-md-6'>
		<p>You currently have {$_SESSION['you']['amount']}$ in your account.</p>
		<p>You transferred a total of {$_SESSION['winrar']['amount']}$ to WinRAR.</p><br/>";
	if ($_SESSION['winrar']['amount'] >= 300) {
		echo "<code>".getenv('FLAG')."</code>";
	}
	echo "</div>";

	echo "<div class='col-md-6'><p>Create a new payment</p>
		<form action='authorize_payment.php' method='GET'>
			<label for='amount' value='Amount'>
			<input type='text' name='amount' placeholder='0'/>
			<input type='submit' class='btn btn-primary'/>
		</form></div>";
} else {
	echo "<div class='col-md'>You currently don't have an account</div>";
}

echo "<div class='col-md'>Go <a href='new_account.php'>here</a> if you want a new account.</div>";


include 'includes/footer.php';

?>

