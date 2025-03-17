function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function displayMessages(data = {}) {
  if (!data["error"] && !data["success"]) return;
  let message = document.createElement("li");
  let close_button = document.createElement("button");
  close_button.className = "close";
  close_button.dataset.dismiss = "alert";
  close_button.innerHTML = '<span aria-hidden="true">&times;</span>';
  if (data["error"]) {
    message.className = "alert alert-danger alert-dismissable fade show";
    message.role = "alert";
    message.textContent = data["error"];
  } else if (data["success"]) {
    message.className = "alert alert-success alert-dismissable fade show";
    message.role = "alert";
    message.textContent = data["success"];
  }
  message.appendChild(close_button);
  document.getElementById("messages").appendChild(message);
}

function setLikeBtn() {
  let likeBtns = document.querySelectorAll(".like-btn");

  likeBtns.forEach((element) => {
    // attach action for each like button
    element.onclick = (e) => {
      // get link of current post
      const link = element.href;
      e.preventDefault();
      // send like request of current post
      fetch(link, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
        mode: "same-origin",
      })
        .then((response) => response.json())
        .then((data) => {
          // toggle button like of current post
          let child_element = document.getElementById(`like-${element.id}`);
          if (data["like_post"]) {
            child_element.className = "fa fa-heart";
            child_element.style.color = "#dc3545";
          } else {
            child_element.className = "fa fa-heart-o";
            child_element.style.color = "#007bff";
          }
          // update likes count of current post
          document.getElementById(
            `${element.id}-like-count`
          ).textContent = `Likes: ${data["count_likes"]}`;
        })
        .catch((err) => console.log(err));
    };
  });
}
