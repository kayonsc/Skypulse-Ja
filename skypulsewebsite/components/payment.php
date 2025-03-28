<?php
$paypal_url = "https://www.paypal.com/cgi-bin/webscr"; 
$paypal_id = "kayonswabyc@gmail.com"; // Replace with your PayPal email
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pay with PayPal</title>
</head>
<body>

    <h2>Checkout with PayPal</h2>
    
    <form action="<?php echo $paypal_url; ?>" method="post">
        <!-- PayPal Business Email -->
        <input type="hidden" name="business" value="<?php echo $paypal_id; ?>">

        <!-- Specify PayPal Payment Type -->
        <input type="hidden" name="cmd" value="_xclick">

        <!-- Payment Details -->
        <input type="hidden" name="item_name" value="Drone Delivery Service">
        <input type="hidden" name="currency_code" value="USD">
        <label>Amount (USD):</label>
        <input type="number" name="amount" required>
        
        <!-- Return URLs -->
        <input type="hidden" name="return" value="http://localhost/your_project/success.php">
        <input type="hidden" name="cancel_return" value="http://localhost/your_project/cancel.php">

        <button type="submit">Pay with PayPal</button>
    </form>

</body>
</html>