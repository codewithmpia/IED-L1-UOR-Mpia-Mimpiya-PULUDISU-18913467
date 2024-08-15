/* 1. NAVIGATION */
const navigation = {
    elements: {
        tabletProfileOpenIcon: document.querySelector(".tablet-profile-open-icon"),
        tabletProfileData: document.querySelector(".tablet-profile-data"),
        tabletProfileCloseIcon: document.querySelector(".tablet-profile-close-icon"),
        mobileMenuOpenIcon: document.querySelector(".mobile-menu-open-icon"),
        mobileMenu: document.querySelector(".mobile-menu"),
        mobileMenuCloseIcon: document.querySelector(".mobile-menu-close-icon"),
        body: document.querySelector("body"),
    },

    toggleClass: function(element, className, add) {
        if (add) {
            element.classList.add(className);
        } else {
            element.classList.remove(className);
        }
    },

    toggleTabletProfile: function(add) {
        this.toggleClass(this.elements.tabletProfileData, "open", add);
        this.toggleClass(this.elements.body, "no-scroll", add);
        if (!add) {
            document.removeEventListener("click", this.closeOutsideTabletProfile);
        }
    },

    closeOutsideTabletProfile: function(evt) {
        if (!navigation.elements.tabletProfileData.contains(evt.target) && evt.target !== navigation.elements.tabletProfileOpenIcon) {
            navigation.toggleTabletProfile(false);
            evt.stopPropagation();
        }
    },
    
    toggleMobileMenu: function(add) {
        this.toggleClass(this.elements.mobileMenu, "open", add);
        this.toggleClass(this.elements.body, "no-scroll2", add);
        if (!add) {
            this.toggleTabletProfile(false);
        }
    },

    init: function() {
        this.elements.tabletProfileOpenIcon.addEventListener("click", () => this.toggleTabletProfile(true));
        this.elements.tabletProfileCloseIcon.addEventListener("click", () => this.toggleTabletProfile(false));
        this.elements.mobileMenuOpenIcon.addEventListener("click", () => this.toggleMobileMenu(true));
        this.elements.mobileMenuCloseIcon.addEventListener("click", () => this.toggleMobileMenu(false));
        document.addEventListener("click", (evt) => this.closeOutsideTabletProfile(evt));
    },    
};

navigation.init();

/* 2. MESSAGES */
const messages = {
    elements: {
        alerts: document.querySelectorAll(".alert"),
        alertCloseIcons: document.querySelectorAll(".alert-close-icon"),
    },

    closeAlert: function() {
        this.elements.alerts.forEach((alert, index) => {
            this.elements.alertCloseIcons[index].addEventListener("click", () => {
                //alert.parentElement.removeChild(alert);
                alert.style.display = "none";
            });
        });
    }
}

messages.closeAlert();

/* 3. FILTRES PAR CATEGORIE */
const categoriesFilters = {
    elements: {
      categoriesBtn: document.querySelector(".categories-btn"),
      categoriesList: document.querySelector(".categories-list"),
      categoriesItems: document.querySelectorAll(".categories-item"),
      formations: document.querySelectorAll(".formation"),
      categoriesBtnIcon: document.querySelector(".categories-btn-svg"),
      alertElement: document.querySelector(".alert.info"),
    },
  
    totalFormations: 0,
  
    init: function () {
      this.updateNumberPerCategory();
  
      this.elements.categoriesBtn.addEventListener("click", this.onCategoryBtnClick.bind(this));
  
      this.elements.categoriesItems.forEach((item) =>
        item.addEventListener("click", this.onCategoryItemClick.bind(this))
      );
  
      // Ajouter un écouteur événements pour les clics en dehors de la liste des catégories
      document.addEventListener("click", this.onDocumentClick.bind(this));
    },
  
    onDocumentClick: function (event) {
      const targetElement = event.target;
  
      // Vérifier si elément cliqué est en dehors de la liste des catégories
      if (!this.elements.categoriesList.contains(targetElement) && !this.elements.categoriesBtn.contains(targetElement)) {
        this.elements.categoriesList.classList.remove("open");
  
        // Faire pivoter icone
        this.rotateIcon();
      }
    },
  
    updateNumberPerCategory: function () {
      let totalFormations = this.elements.formations.length;
  
      this.totalFormations = totalFormations;
  
      for (const item of this.elements.categoriesItems) {
        const category = item.dataset.category || "";
        const numberElement = item.querySelector(".number-per-category");
  
        if (numberElement) {
          if (category === "") {
            numberElement.textContent = totalFormations;
          } else {
            let count = 0;
  
            for (const formation of this.elements.formations) {
              const formationCategory = formation.getAttribute("category");
  
              if (formationCategory === category) {
                count++;
              }
            }
  
            numberElement.textContent = count;
          }
        }
      }
      this.showAlert();
    },
  
    onCategoryBtnClick: function () {
      this.elements.categoriesList.classList.toggle("open");
  
      // Faire pivoter icone
      this.rotateIcon();
    },
  
    onCategoryItemClick: function (event) {
      // Trouver élément <li> parent
      let parentElement = event.target;
    
      while (parentElement && parentElement.tagName !== "LI") {
        parentElement = parentElement.parentNode;
      }
    
      if (parentElement) {
        const filterValue = parentElement.dataset.category || "";
    
        // Mettre à jour le bouton de catégorie
        const categoryTextElement = parentElement.querySelector(".category-text");
    
        if (categoryTextElement) {
          this.elements.categoriesBtn.querySelector("span:first-child").textContent = categoryTextElement.textContent;
        }
    
        // Fermer la liste de catégories
        this.elements.categoriesList.classList.remove("open");
    
        // Faire pivoter icone
        this.rotateIcon();
    
        let formationsInCategory = 0;
    
        for (const formation of this.elements.formations) {
          if (filterValue === "") {
            formation.style.display = "block";
            formationsInCategory += 1;
          } else {
            const category = formation.getAttribute("category");
            formation.style.display = category === filterValue ? "block" : "none";
    
            if (category === filterValue) {
              formationsInCategory += 1;
            }
          }
        }
    
        if (formationsInCategory === 0) {
          const alertContent = this.elements.alertElement.querySelector("strong:first-child");
          if (filterValue === "") {
            alertContent.textContent = "Pas de formations disponibles";
          } else {
            alertContent.textContent = "Cette catégorie ne contient pas de formations.";
          }
          this.elements.alertElement.style.display = "flex";
    
        } else {
          this.elements.alertElement.style.display = "none";
        }
      }
    },
    
  
    rotateIcon: function () {
      if (this.elements.categoriesList.classList.contains("open")) {
        this.elements.categoriesBtnIcon.classList.add("rotate-180");
      } else {
        this.elements.categoriesBtnIcon.classList.remove("rotate-180");
      }
    },
  
    showAlert: function () {
      if (this.totalFormations === 0) {
        this.elements.alertElement.style.display = "flex"
      } else {
        this.elements.alertElement.style.display = "none"
      }
    },
  };


categoriesFilters.init();

