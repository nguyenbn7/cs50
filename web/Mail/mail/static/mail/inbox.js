document.addEventListener("DOMContentLoaded", function (e) {
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
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#content-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  document.querySelector("#compose-form").onsubmit = (e) => {
    const recipients = document
      .getElementById("compose-recipients")
      .value.trim();
    const subject = document.getElementById("compose-subject").value.trim();
    const body = document.getElementById("compose-body").value.trim();
    e.preventDefault();
    if (recipients === "" || subject === "" || body === "") {
      display_message((message = { error: "Input can not be empty" }));
    } else {
      fetch("/emails", {
        method: "POST",
        body: JSON.stringify({
          // context body for post request
          recipients: recipients,
          subject: subject,
          body: body,
        }),
      })
        .then((response) => response.json())
        .then((message) => {
          const isSucess = message["error"] ? false : true;
          if (isSucess) {
            window.onload = load_mailbox("sent");
          }
          display_message(message);
        })
        .catch((err) => console.log(err));
    }
  };

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function display_message(message = "") {
  let message_element = document.createElement("span");
  if (message["error"]) {
    message_element.className = "alert alert-danger";
    message_element.textContent = message["error"];
  } else if (message["message"]) {
    message_element.className = "alert alert-success";
    message_element.textContent = message["message"];
  }
  // remove alert after 1s
  const timeout = 1000;
  setTimeout(() => {
    message_element.remove();
  }, timeout);
  document.getElementById("message").appendChild(message_element);
  window.scrollTo(0, 0);
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  let emails_view = document.querySelector("#emails-view");
  emails_view.style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#content-view").style.display = "none";

  // Show the mailbox name
  emails_view.innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      emails.forEach((email) => {
        // Create mail box row
        let row = document.createElement("div");
        row.className = "row mb-2";

        // create mail box element
        let mailbox_element = document.createElement("div");
        mailbox_element.className =
          "col border border-secondary rounded p-3 mailbox";

        if (email["read"] === true) {
          mailbox_element.classList.add("read");
        }

        // fill mail box with infomation
        mailbox_element.innerHTML += `<div class="row">
        <span class="col"><b>${email["sender"]}</b></span><span class="col-6">${email["subject"]}</span><span class="col">${email["timestamp"]}</span>
        </div>`;

        // when user click mail box, load content of that mail
        mailbox_element.addEventListener("click", (e) => {
          fetch(`/emails/${email["id"]}`, {
            method: "PUT",
            body: JSON.stringify({ read: true }),
          });
          load_content(email);
        });
        row.appendChild(mailbox_element);

        // create archieve button for each mail
        if (mailbox !== "sent") {
          let archived_btn = document.createElement("button");

          if (!email["archived"]) {
            archived_btn.textContent = "archive";
            archived_btn.className =
              "btn btn-outline-primary col-1 text-justify";
          } else {
            archived_btn.textContent = "archived";
            archived_btn.className =
              "btn btn-outline-danger col-1 text-justify";
          }

          // add click event for each mail, if button is pressed then send signal that mail is archieved
          archived_btn.addEventListener("click", (e) => {
            let body = {};
            if (e.target.textContent.toLowerCase() === "archive")
              body["archived"] = true;
            else if (e.target.textContent.toLowerCase() === "archived")
              body["archived"] = false;

            e.currentTarget.parentNode.style.animationPlayState = "running";
            e.currentTarget.parentNode.addEventListener(
              "animationend",
              (element) => {
                element.currentTarget.remove();
              }
            );

            fetch(`/emails/${email["id"]}`, {
              method: "PUT",
              body: JSON.stringify(body),
            });
          });

          row.appendChild(archived_btn);
        }

        emails_view.appendChild(row);
      });
    })
    .catch((err) => console.log(err));
}

function load_content(mail) {
  // Show content of mail and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#content-view").style.display = "block";
  document.querySelector("#content-view").innerHTML = "";

  // top of mail content
  document.querySelector(
    "#content-view"
  ).innerHTML += `<div><b>From:</b> ${mail["sender"]}</div><div><b>To:</b> ${mail["recipients"][0]}</div><div><b>Subject:</b> ${mail["subject"]}</div><div><b>Timestamp:</b> ${mail["timestamp"]}</div>`;

  // create reply button
  let reply_btn = document.createElement("button");
  reply_btn.className = "btn btn-outline-primary";
  reply_btn.textContent = "Reply";

  reply_btn.addEventListener("click", () => {
    compose_reply(mail);
  });
  document.querySelector("#content-view").appendChild(reply_btn);

  // body of mail content
  document
    .querySelector("#content-view")
    .appendChild(document.createElement("hr"));
  let mail_body = document.createElement("textarea");
  mail_body.className = "w-100";
  mail_body.setAttribute("disabled", true);
  mail_body.textContent = mail["body"];

  document.querySelector("#content-view").appendChild(mail_body);
}

function compose_reply(mail) {
  // load form first
  compose_email();

  // fill form with information of mail
  document.querySelector("#compose-recipients").value = `${mail["sender"]}`;

  if (mail["subject"].substring(0, 4) !== "Re: ")
    document.querySelector("#compose-subject").value = `Re: ${mail["subject"]}`;
  else document.querySelector("#compose-subject").value = `${mail["subject"]}`;

  document.querySelector(
    "#compose-body"
  ).value = `On ${mail["timestamp"]} ${mail["sender"]} wrote: ${mail["body"]}\n`;
  document.querySelector(
    "#compose-body"
  ).value += `------------------------------------------------------------------------`;
}
