# Create Technical User

When you use Access Policies to protect your artifacts from unwanted access, you need to provide a technical user for CICD Actions. Due to activated Access Policies, the CI/CD workflows require a dedicated technical user to be able to access the protected objects.

> **Note:** Repeat these steps for every tenant in your landscape (DEV, TST, PRD).

---

## 📋 Prerequisites

- Access to your Identity Management System (e.g., SAP Identity Authentication Service) connected to BTP
- Administrator permissions in SAP BTP Cockpit to assign Role Collections
- A service instance with **Password Grant** enabled (see [Create Service Key](create-service-key.md))

---

## 🔧 Step-by-Step Instructions

### Step 1: Create the Technical User

Create a dedicated technical user in your Identity Management System connected to BTP:

1. Navigate to your Identity Provider administration console
2. Create a new user with a meaningful name (e.g., `cicd-technical-user-dev@yourdomain.com`)
3. Ensure **basic authentication** is activated for this user
4. Set a secure password and store it safely

> ⚠️ **Important:** A dedicated technical user must be created for **every tenant** (DEV, TST, PRD) in your landscape. Use a consistent naming convention, for example:
> - DEV: `cicd-technical-user-dev@yourdomain.com`
> - TST: `cicd-technical-user-tst@yourdomain.com`
> - PRD: `cicd-technical-user-prd@yourdomain.com`

### Step 2: Assign Access Policies via Role Collection

To grant the technical user access to your protected Integration Suite artifacts:

1. Navigate to your subaccount in the **SAP BTP Cockpit**
2. Go to **Security → Role Collections**
3. Create or select a Role Collection that includes the required Access Policies
4. Assign the Role Collection to your technical user

### Step 3: Configure Service Instance for Password Grant

When creating the service instance (see [Create Service Key](create-service-key.md)), ensure you select **Password Grant** in addition to the other required roles. This enables the technical user to authenticate via username and password.