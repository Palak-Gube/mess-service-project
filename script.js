// ---------------------
// Page Loader with Navigation
// ---------------------
function loadPage(page, element) {
  fetch(page)
    .then(response => response.text())
    .then(data => {
      // Load the page content into the container
      document.getElementById("dashboard-container").innerHTML = data;

      // Update active link in sidebar/nav
      document.querySelectorAll(".nav-links a").forEach(link => link.classList.remove("active"));
      if(element) element.classList.add("active");

      // After content is loaded, update username and today's menu
      updateUserName();
      loadTodaysMenu();
    });
}

// Load default dashboard on first load
window.onload = () => loadPage('dashboard-content.html', document.querySelector('.nav-links a'));

// ---------------------
// Function to display logged-in username
// ---------------------
function updateUserName() {
  const usernameElement = document.getElementById("user-name");
  if(usernameElement) {
    const username = localStorage.getItem("loggedInUser") || "User";
    usernameElement.innerText = username;
  }
}

// ---------------------
// Function to display today's menu dynamically
// ---------------------
function loadTodaysMenu() {
  const weeklyMenu = {
    Monday: {
      Breakfast: "Pancakes, Fruit Juice, Tea/Coffee",
      Lunch: "Veg Biryani, Raita, Salad",
      Dinner: "Paneer Butter Masala, Roti, Rice"
    },
    Tuesday: {
      Breakfast: "Omelette, Toast, Tea/Coffee",
      Lunch: "Chole Bhature, Salad",
      Dinner: "Dal Tadka, Jeera Rice, Veg Curry"
    },
    Wednesday: {
      Breakfast: "Idli, Sambar, Coconut Chutney",
      Lunch: "Vegetable Pulao, Curd",
      Dinner: "Rajma, Rice, Salad"
    },
    Thursday: {
      Breakfast: "Poha, Tea",
      Lunch: "Matar Paneer, Roti, Rice",
      Dinner: "Chicken Curry, Rice, Salad"
    },
    Friday: {
      Breakfast: "Paratha, Pickle, Tea/Coffee",
      Lunch: "Veg Khichdi, Raita",
      Dinner: "Fish Curry, Rice, Veg Stir Fry"
    },
    Saturday: {
      Breakfast: "Dosa, Coconut Chutney",
      Lunch: "Paneer Biryani, Salad",
      Dinner: "Mixed Veg Curry, Roti, Rice"
    },
    Sunday: {
      Breakfast: "French Toast, Fruit Salad",
      Lunch: "Mutton Curry, Rice, Roti",
      Dinner: "Light Soup, Sandwiches"
    }
  };

  const days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
  const today = new Date();
  const todayName = days[today.getDay()];

  // Display the date in "Today's Menu" header
  const todayDateElement = document.getElementById("today-date");
  if(todayDateElement) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    todayDateElement.innerText = `Today's Menu (${today.toLocaleDateString(undefined, options)})`;
  }

  // Display meals
  const menuDiv = document.getElementById("menu");
  if(menuDiv) {
    menuDiv.innerHTML = ""; // Clear old content
    const todayMenu = weeklyMenu[todayName];

    for (const meal in todayMenu) {
      const mealDiv = document.createElement("div");
      mealDiv.className = "meal-item";

      const mealTitle = document.createElement("h4");
      mealTitle.innerText = meal;
      mealDiv.appendChild(mealTitle);

      const mealContent = document.createElement("p");
      mealContent.innerText = todayMenu[meal];
      mealDiv.appendChild(mealContent);

      menuDiv.appendChild(mealDiv);
    }
  }
}
