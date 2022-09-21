

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // Create an instance of the Stripe object with your publishable API key
    const stripe = Stripe("{{ STRIPE_PUBLIC_KEY }}");
    const checkoutButton = document.getElementById("checkout-button");
    checkoutButton.addEventListener("click", function () {
      fetch("{% url 'create-checkout-session' product.id %}", {
        method: "POST",
        headers: {
            'X-CSRFToken': csrftoken
        }
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (session) {
          return stripe.redirectToCheckout({ sessionId: session.id });
        })
        .then(function (result) {
          // If redirectToCheckout fails due to a browser or network
          // error, you should display the localized error message to your
          // customer using error.message.
          if (result.error) {
            alert(result.error.message);
          }
        })
        .catch(function (error) {
          console.error("Error:", error);
        });
    });

    // Disable the button until we have Stripe set up on the page
    document.querySelector("button").disabled = true;

    const elements = stripe.elements();
    const style = {
        base: {
            color: "#32325d",
            fontFamily: 'Arial, sans-serif',
            fontSmoothing: "antialiased",
            fontSize: "16px",
            "::placeholder": {
                color: "#32325d"
            }
        },
        invalid: {
            fontFamily: 'Arial, sans-serif',
            color: "#fa755a",
            iconColor: "#fa755a"
        }
    };
    const card = elements.create("card", {style: style});
    // Stripe injects an iframe into the DOM
    card.mount("#card-element");
    card.on("change", function (event) {
      // Disable the Pay button if there are no card details in the Element
      document.querySelector("button").disabled = event.empty;
      document.querySelector("#card-error").textContent = event.error ? event.error.message : "";
    });
    const form = document.getElementById("payment-form");


    // Calls stripe.confirmCardPayment
    // If the card requires authentication Stripe shows a pop-up modal to

    /* ------- UI helpers ------- */

    // Show a spinner on payment submission
    const loading = function(isLoading) {
      if (isLoading) {
        // Disable the button and show a spinner
        document.querySelector("button").disabled = true;
        document.querySelector("#spinner").classList.remove("hidden");
        document.querySelector("#button-text").classList.add("hidden");
      } else {
        document.querySelector("button").disabled = false;
        document.querySelector("#spinner").classList.add("hidden");
        document.querySelector("#button-text").classList.remove("hidden");
      }
    };
    // Shows a success message when the payment is complete
    const orderComplete = function(paymentIntentId) {
      loading(false);
      document
        .querySelector(".result-message a")
        .setAttribute(
          "href",
          "https://dashboard.stripe.com/test/payments/" + paymentIntentId
        );
      document.querySelector(".result-message").classList.remove("hidden");
      document.querySelector("button").disabled = true;
    };

    // Show the customer the error from Stripe if their card fails to charge
    const showError = function(errorMsgText) {
      loading(false);
        const errorMsg = document.querySelector("#card-error");
        errorMsg.textContent = errorMsgText;
      setTimeout(function() {
        errorMsg.textContent = "";
      }, 4000);
    };
    // prompt the user to enter authentication details without leaving your page.
    const payWithCard = function(stripe, card, clientSecret) {
      loading(true);
      stripe
        .confirmCardPayment(clientSecret, {
          payment_method: {
            card: card
          }
        })
        .then(function(result) {
          if (result.error) {
            // Show error to your customer
            showError(result.error.message);
          } else {
            // The payment succeeded!
            orderComplete(result.paymentIntent.id);
          }
        });
    };
    form.addEventListener("submit", function(event) {
      event.preventDefault();
      // Complete payment when the submit button is clicked
      fetch("{% url 'create-payment-intent' product.id %}", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
          email: document.getElementById('email').value
        })
      })
        .then(function(result) {
          return result.json();
        })
        .then(function(data) {
          payWithCard(stripe, card, data.clientSecret);
        });
    });
