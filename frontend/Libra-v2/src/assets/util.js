export function downloadCSVLibrarian() {
  let headers = {
    "Content-Type": "application/pdf",

    Authorization: `Bearer ${localStorage.getItem("jwt")}`,
  };
  if (!localStorage.getItem("jwt")) {
    this.$router.push("/librarian/login");
  }
  axios
    .get(`http://127.0.0.1:5000/librarian/download_report`, {
      headers: headers,
      responseType: "blob",
    })
    .then((data) => {
      console.log(data);
      const blob = data.data;
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `data.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    })
    .catch((err) => {
      console.log(err);
      if (err.response.data.invalid) {
        this.$router.push("/user/login");
        return;
      }
      if (err.response.status === 404) {
        alert("Book does not exist");
      } else if (err.response.status === 403) {
        alert("Access Denied");
      }
    });
}
