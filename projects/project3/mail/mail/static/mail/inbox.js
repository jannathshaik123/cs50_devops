document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document
    .querySelector("#compose")
    .addEventListener("click", () => compose_email());

  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";

  // Focus on the recipients field
  document.querySelector("#compose-recipients").focus();

  // Add event listener for the send button
  document.querySelector("#send-button").addEventListener("click", function () {
    const emailData = {
      recipients: document.querySelector("#compose-recipients").value,
      subject: document.querySelector("#compose-subject").value,
      body: document.querySelector("#compose-body").value,
    };

    fetch("/emails", {
      method: "POST",
      body: JSON.stringify(emailData),
    })
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
        alert(result.error || "Email sent successfully!");
      });
    // After sending, load the sent mailbox
    load_mailbox("sent");
  });
}

function view_email(email_id, mailbox) {
  // Show the email view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#email-view").style.display = "block";

  // Set visibility based on mailbox type
  // If the mailbox is "sent", the archive button should be invisible
  var visible = "visible";
  if (mailbox === "sent") {
    visible = "invisible";
  }

  // Fetch the email details
  fetch("/emails/" + email_id)
    .then((response) => response.json())
    .then((email) => {
      // Mark the email as read
      fetch("/emails/" + email_id, {
        method: "PUT",
        body: JSON.stringify({ read: true }),
      });
      // Print the email details
      console.log(email);

      document.querySelector("#email-view").innerHTML = `
        <div class="card ">
          <div class="card-header">
            <strong>From:</strong> ${email.sender} <br>
            <strong>To:</strong> ${email.recipients} <br>
            <strong>Subject:</strong> ${email.subject} <br>
            <small>${email.timestamp}</small>
          </div>
          <div class="card-body">
            <p>${email.body}</p>
          </div>
          <div class="card-footer">
            <button class="btn btn-primary" onclick="reply_email(${
              email.id
            })">Reply</button>
            <button class="btn btn-secondary ${visible}" onclick="archive_email(${
        email.id
      }, ${!email.archived})">
              ${email.archived ? "Unarchive" : "Archive"}
            </button
          </div>
        </div>`;
    });
}

function archive_email(email_id, archive) {
  // Archive or unarchive the email
  fetch("/emails/" + email_id, {
    method: "PUT",
    body: JSON.stringify({ archived: archive }),
  });
  // Reload the mailboxes
  window.location.reload();
}

function reply_email(email_id) {
  // Fetch the email details
  fetch("/emails/" + email_id)
    .then((response) => response.json())
    .then((email) => {
      // Show compose view
      compose_email();

      // Pre-fill the compose fields with the email details
      document.querySelector("#compose-recipients").value = email.sender;
      document.querySelector("#compose-subject").value =
        email.subject.startsWith("Re: ")
          ? email.subject
          : "Re: " + email.subject;
      document.querySelector(
        "#compose-body"
      ).value = `On ${email.timestamp}, ${email.sender} wrote:\n${email.body}\n\n`;
    });
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  fetch("/emails/" + mailbox)
    .then((response) => response.json())
    .then((emails) => {
      // Print emails
      console.log(emails);
      emails.forEach((email) => {
        const color = email.read ? "bg-light" : "bg-white";
        const emailElement = document.createElement("div");
        emailElement.className = "email-item";
        emailElement.innerHTML = `<div class="border rounded">
                <div class="${color} p-3 border-bottom d-flex justify-content-between align-items-center" onclick="view_email(${email.id}, '${mailbox}')">
                    <div class="email-content">
                        <strong class="me-3">${email.sender}</strong>
                        <span class="text-dark">${email.subject}</span>
                    </div>
                    <small class="text-muted">${email.timestamp}</small>
                </div>
            </div>`;
        document.querySelector("#emails-view").append(emailElement);
      });
    });
}
