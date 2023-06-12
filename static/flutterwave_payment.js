const phonenumber = document.getElementById("phone_number").value
const amount = document.getElementById('amount').value
const user = document.getElementById('user').value
const email = document.getElementById('email').value
const IP = document.getElementById('IP').value
const tx_ref = "S&T" + Math.floor((Math.random() * 9000000000) + 1)


const makePayment = () => {
  FlutterwaveCheckout({
    public_key: "FLWPUBK_TEST-adc8c6446cec882e64d2c80870dfa898-X",
    tx_ref: tx_ref,
    amount: amount,
    currency: "NGN",
    payment_options: "card, mobilemoneyghana, ussd",
    redirect_url: "http://localhost:8000/verify-payment/",
    // redirect_url: "/verify-payment/",
    customer: {
      email: email,
      phone_number: phonenumber,
      name: user,
    },
    customizations: {
      title: "S & T Production",
      description: "Payment for an item'(s)",
      // logo: "https://www.logolynx.com/images/logolynx/22/2239ca38f5505fbfce7e55bbc0604386.jpeg",
    },
  })
}
