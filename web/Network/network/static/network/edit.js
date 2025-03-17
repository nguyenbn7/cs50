document.addEventListener("DOMContentLoaded", (e) => {
  document.getElementById("editpost").onsubmit = (e) => {
    e.preventDefault();
    const content = document.getElementById("content").value;

    fetch(`${e.currentTarget.action}`, {
      method: "POST",
      body: JSON.stringify({
        content: content,
      }),
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      mode: "same-origin",
    })
      .then((res) => res.json())
      .then((data) => displayMessages(data))
      .catch((err) => console.log(err));
  };
});
