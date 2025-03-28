<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require 'vendor/autoload.php'; // Ensure PHPMailer is installed

// Customer's email (should be retrieved dynamically)
$customer_email = "customer@example.com"; // Replace with actual email

$mail = new PHPMailer(true);

try {
    // SMTP Configuration
    $mail->isSMTP();
    $mail->Host = 'smtp.gmail.com'; // Use your email provider's SMTP server
    $mail->SMTPAuth = true;
    $mail->Username = 'your-email@gmail.com'; // Replace with your email
    $mail->Password = 'your-email-password'; // Replace with your email password
    $mail->SMTPSecure = 'tls';
    $mail->Port = 587;

    // Email Details
    $mail->setFrom('your-email@gmail.com', 'Drone Delivery Service');
    $mail->addAddress($customer_email); 
    $mail->Subject = 'Delivery Confirmation';
    $mail->Body = "Hello,\n\nYour package has been successfully delivered!\n\nThank you for choosing our drone delivery service.";

    // Send Email
    $mail->send();
    echo "Delivery confirmation email sent successfully!";
} catch (Exception $e) {
    echo "Email sending failed: {$mail->ErrorInfo}";
}
?>