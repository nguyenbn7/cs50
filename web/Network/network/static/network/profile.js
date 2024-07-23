document.addEventListener("DOMContentLoaded", (e) => {
  followButton();
  setLikeBtn();
});

function followButton() {
  const followBtn = document.getElementById("follow");
  if (!followBtn) return;
  followBtn.onclick = (e) => {
    const current_user = e.currentTarget.dataset.user;

    fetch(`/follow`, {
      method: "POST",
      body: JSON.stringify({
        user: current_user,
      }),
      // get csrf token
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      mode: "same-origin",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data["error"]) {
          displayMessages(data);
          return;
        }
        // toggle button follow of profile
        if (data["toggle_follow_btn"] !== undefined) {
          if (data["toggle_follow_btn"]) {
            followBtn.className = "btn btn-danger";
            followBtn.textContent = "Unfollow";
          } else {
            followBtn.className = "btn btn-primary";
            followBtn.textContent = "Follow";
          }
        }

        // update status for the number of follwers and the number of user following other users of current profile
        document.getElementById(
          "follower"
        ).textContent = `Follower: ${data["count_people_follow_profile_user"]}`;
        document.getElementById(
          "following"
        ).textContent = `Following: ${data["count_people_profile_user_follows"]}`;
      })
      .catch((err) => console.log(err));
  };
}
