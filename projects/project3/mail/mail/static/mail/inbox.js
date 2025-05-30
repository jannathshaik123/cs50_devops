document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Focus on the recipients field
  document.querySelector('#compose-recipients').focus();

  // Add event listener for the send button
  document.querySelector('#send-button').addEventListener('click', function() {
    const emailData = {
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    };

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify(emailData)
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      alert(`Email sent to ${emailData.recipients}`);
      load_mailbox('sent');
    });
  
  });
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch('/emails/inbox')
  .then(response => response.json())
  .then(emails => {
    // Print emails
    console.log(emails);
    emails.forEach(email => {
      const emailElement = document.createElement('div');
      emailElement.className = 'email-item';
      emailElement.innerHTML = `<span class="border border-secondary rounded-3"><strong>${email.sender}</strong> - ${email.subject} <span class="email-date">${email.timestamp}</span></span>`;
      document.querySelector('#emails-view').append(emailElement);
    });
});
}