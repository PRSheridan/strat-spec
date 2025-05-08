Draft

An application for cataloging searching for and identifying Stratocaster models. 

install dependencies

bun run dev
pipenv shell && cd server
python app.py

OR

./start.sh

### **Guitar Catalog & Models System**

- **User-Guitars:** Users can upload guitars with full specifications.
- **Models:** Official guitars with fixed (variable) specifications, created by promoted user-guitars OR manually.

---

### **Pages & Navigation**

- **Catalogue Page:** Lists user-guitars with filtering and sorting options.
- **Guitar Specs Page:** Displays a user-guitar; if it matches a model, links to the model’s specs page.
- **Model Specs Page:** Displays official models with fixed specifications.
- **Profile Pages:** Each user has a profile listing their guitars and a bio.

---

### **User Access & Permissions**

- **Visitors (No Account):**
    - Browse the catalogue of guitars
- **Registered Users:**
    - Browse the catalogue of guitars
    - Upload/manage their guitars
    - Favorite and comment on guitar
    - Edit account
- **Admins:**
    - Can manage other users, including their guitars.
    - Have a maintenance page to manually approve guitar promotions to models.

---

### **Engagement & Social Features**

- **Activity Feed:** Shows recent guitar uploads.
- **Commenting & Rating System:** Users can leave feedback on user-created guitars.
- **Tagging System:** Users can tag guitars to improve discoverability.
- **Favorite Collections:** Users can organize favorited guitars into collections.

---

### **Model Promotion System**

- **Automatic Flagging:** The system detects user-guitars that match common specifications and flags them for potential model status.
- **Admin Review:** Admins can review flagged guitars and manually approve them as models.
- **"Suggest as Model":** Users can recommend a guitar for model consideration, alerting admins.


