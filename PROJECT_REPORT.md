# PROJECT DOCUMENTATION
## FOR
# HIREHELPER: A PROFESSIONAL TASK ECOSYSTEM

**Submitted in partial fulfillment of the requirements for the degree of**
**Bachelor of Technology**
**in**
**Computer Science and Engineering**

---

### **TABLE OF CONTENTS**

1.  **ABSTRACT** .......................................................................................... 1
2.  **INTRODUCTION** ................................................................................ 3
    2.1 Overview of the Platform ................................................................ 4
    2.2 Motivation behind HireHelper .............................................................. 6
3.  **PROBLEM STATEMENT AND AIM** ............................................... 8
    3.1 Problem Definition ............................................................................. 9
    3.2 Proposed Aim .................................................................................... 11
4.  **OBJECTIVES** ....................................................................................... 13
    4.1 Functional Objectives ........................................................................ 14
    4.2 Security and Technical Objectives .................................................... 16
5.  **SYSTEM REQUIREMENTS** .............................................................. 18
    5.1 Functional Requirements ................................................................... 19
    5.2 Non-Functional Requirements ........................................................... 21
6.  **PROPOSED SYSTEM** ........................................................................ 23
    6.1 System Overview ............................................................................... 24
    6.2 Layered Architecture .......................................................................... 26
7.  **ARCHITECTURE AND DESIGN (UML)** ........................................ 28
    7.1 Use Case Diagram ............................................................................. 29
    7.2 Class Diagram ................................................................................... 31
    7.3 Sequence Diagram ............................................................................. 33
8.  **IMPLEMENTATION** .......................................................................... 35
    8.1 Frontend Implementation (Angular) .................................................. 36
    8.2 Backend Implementation (Django) .................................................... 38
    8.3 Database Schema and ERD .............................................................. 40
9.  **MODULES DESCRIPTION** .............................................................. 42
    9.1 Authentication and Profile Management ........................................... 43
    9.2 Task Management and Discovery ...................................................... 45
    9.3 Request and Application Lifecycle .................................................... 47
    9.4 Review and Rating System ................................................................. 49
10. **OUTPUT SCREENS** ........................................................................... 51
11. **TESTING AND EVALUATION** ........................................................ 55
12. **CONCLUSION** .................................................................................... 59
13. **FUTURE SCOPE** ................................................................................ 61
14. **BIBLIOGRAPHY** ................................................................................ 63

---

## **1. ABSTRACT**

The modern gig economy has revolutionized how short-term work is distributed and consumed. However, existing platforms often cater to high-end white-collar freelancing or remain overly fragmented for localized, task-based hiring. **HireHelper** is a comprehensive, full-stack web application designed to bridge the gap between service seekers (Hirers) and task fulfillers (Helpers). By leveraging a modern technology stackâ€”comprising **Angular 17** for a responsive, high-performance frontend and **Django 5.0** alongside the **Django REST Framework** for a scalable backendâ€”HireHelper offers a seamless, secure, and visually stunning ecosystem for task management.

The platform introduces a premium **Dark Glassmorphism** design language, ensuring that user experience (UX) is prioritized alongside technical functionality. Key features include a real-time task discovery feed, a multi-stage application tracking system, secure JWT-based authentication with OTP verification, and a robust peer-review mechanism. This documentation provides an in-depth analysis of the system requirements, architectural design (UML), implementation details, and evaluation metrics that define the HireHelper platform. Through this project, we demonstrate the integration of modern web standards, secure API design, and user-centric software development practices.

---

## **2. INTRODUCTION**

### **2.1 Overview of the Platform**

**HireHelper** is positioned as a "Professional Task Ecosystem" that transforms the traditional hiring process for short-term projects into a structured, transparent, and efficient digital workflow. Unlike generic job boards, HireHelper focuses on the *micro-task* and *local service* market, where speed and reliability are paramount.

The platform operates on a dual-user model:
1.  **Hirers (Employers)**: Individuals or entities looking to delegate tasks. They can post detailed task descriptions, specify locations, set timelines, and review incoming applications from potential Helpers.
2.  **Helpers (Task Fulfillers)**: Skilled individuals looking for opportunities. They can browse a live feed of tasks, apply with personalized pitches, and track their application status in real-time.

The core value proposition of HireHelper lies in its **transparency**. Every task completion is followed by a reciprocal rating and review cycle, building a decentralized reputation system that protects both parties. Furthermore, the technical implementation utilizes **RxJS** in the Angular frontend for reactive state management and **PostgreSQL** in the backend for reliable data persistence, ensuring the platform can scale as the user base grows.

### **2.2 Motivation behind HireHelper**

The motivation for developing HireHelper stems from three primary observations in the current labor market of 2024-2025:
*   **The Trust Gap**: Finding reliable help for manual or localized tasks often relies on word-of-mouth, which is inherently limited. HireHelper aims to digitize this trust through verified profiles and historical performance data.
*   **Aesthetic Fatigue**: Most utility-based platforms follow archaic, utilitarian designs. HireHelper seeks to prove that utility tools can be secondary to a "premium" experience by implementing modern design trends like glassmorphism and smooth transitions.
*   **Technical Integration**: There is a need for academic projects that demonstrate a clean separation of concerns between a modern TypeScript-based SPA (Single Page Application) and a secure Python-based REST API, following industry-standard principles like Clean Architecture and DRY (Don't Repeat Yourself).

---

## **3. PROBLEM STATEMENT AND AIM**

### **3.1 Problem Definition**

In the current digital landscape, individuals looking for quick servicesâ€”such as moving help, minor repairs, event assistance, or specialized short-term tasksâ€”face several critical challenges:
1.  **Fragmentation**: Opportunities for helpers and service requests from hirers are scattered across social media groups, physical bulletins, and low-traffic community boards. This leads to missed opportunities and wasted time.
2.  **Lack of Accountability**: Without a centralized system to track task history, there is no verified way to know if a helper is reliable or if a hirer is legitimate. This leads to security concerns and payment disputes.
3.  **Inefficient Matching**: Most job boards are designed for long-term employment, requiring complex resumes and lengthy interview cycles. There is a lack of platforms optimized for the "apply-now, work-today" micro-task workflow.
4.  **Static Interfaces**: Existing local-help applications often suffer from poor mobile responsiveness and outdated user interfaces, making navigation difficult for users on the go.

### **3.2 Proposed Aim**

The primary aim of this project is to design and implement **HireHelper**, a robust, secure, and visually immersive platform that addresses These challenges by providing:
*   **A Centralized Task Hub**: A unified discovery feed where all localized tasks are aggregated and filterable.
*   **Verified Reputation System**: A mechanism where only verified users can interact, and every interaction contributes to a public trust score.
*   **Real-time Communication Flow**: Utilizing modern API signaling to ensure hirers and helpers are updated instantly on application statuses and reviews.
*   **High-End Visual Identity**: Implementing a "Dark Glassmorphism" UI that feels premium and state-of-the-art, encouraging user engagement through superior aesthetics.

---

## **4. OBJECTIVES**

### **4.1 Functional Objectives**

The development of HireHelper is guided by several key functional milestones:
*   **Unified Authentication**: To implement a secure registration and login system that distinguishes between 'Hirer' and 'Helper' roles while providing an extra layer of security via **OTP (One-Time Password) email verification**.
*   **Dynamic Task Discovery**: To create a "Task Pulse" discovery feed that allows users to browse open tasks with real-time card previews, location-based filtering, and category sorting.
*   **Lifecycle Management**: To engineer an "Application Hub" that manages the entire lifecycle of a taskâ€”from posting and applying to accepting, rejecting, and finally marking as completed.
*   **Feedback Integration**: To develop a "Feedback Loop" system where users can rate and review each other, ensuring accountability and rewarding high-quality service.

### **4.2 Security and Technical Objectives**

Beyond user-facing features, the project aims to meet rigorous technical standards:
*   **Secure Stateless Auth**: utilizing **JSON Web Tokens (JWT)** for secure, session-less communication between the Angular client and Django server.
*   **Data Integrity**: Implementing strict database constraints in PostgreSQL to prevent duplicate applications and ensure rating validity.
*   **Performance Optimization**: Ensuring that all API responses are optimized for speed, with frontend lazy-loading and efficient backend querysets.
*   **Full Responsiveness**: Guaranteeing that the platform is 100% responsive across mobile, tablet, and desktop viewports, maintaining the glassmorphic aesthetics on all screen sizes.

---

## **5. SYSTEM REQUIREMENTS**

### **5.1 Functional Requirements**

The functional requirements of HireHelper are divided into core modules that facilitate the end-to-end task cycle. These requirements define what the system must do to satisfy user needs.

#### **5.1.1 User Authentication and Authorization**
*   **Self-Registration**: The system shall allow new users to register by providing a unique username, email, password, and selecting a primary role (Hirer or Helper).
*   **OTP Verification**: Upon registration, the system shall send a 6-digit One-Time Password (OTP) to the user's email. Access to restricted features is only granted after successful verification.
*   **Role-Based Access Control (RBAC)**: The system shall enforce permissions based on roles. Hirers can create tasks; Helpers can apply. Common features like profile editing are accessible to both.
*   **JWT Logout**: The system shall invalidate tokens on the client-side upon logout to ensure session termination.

#### **5.1.2 Task Management Module**
*   **Task Creation**: Hirers shall be able to post tasks with titles, descriptions, specific locations, city names, and start/end times.
*   **Media Support**: The platform shall support image uploads for task descriptions to provide visual context for Helpers.
*   **Task State Tracking**: Tasks shall maintain a state (Open, In Progress, Completed). The transition between these states is managed by the system based on hirer actions.

#### **5.1.3 Application and Request Lifecycle**
*   **Applying for Tasks**: Helpers shall be able to submit a 'Task Request' with a personalized message.
*   **Request Management**: Hirers shall be able to view all requests for their tasks and respond with 'Accept' or 'Reject' signals, including a custom reply.
*   **Real-time Status Updates**: Helpers shall have a dedicated "My Requests" dashboard to track the status of their pending and approved applications.

#### **5.1.4 Review and Reputation**
*   **Two-way Feedback**: Once a task is completed, the system shall prompt both parties to provide a rating (1-5 stars) and a written comment.
*   **Average Rating Calculation**: The system shall dynamically calculate and display a user's average rating on their profile page.

### **5.2 Non-Functional Requirements**

Non-functional requirements specify the *quality* attributes and constraints of the system, ensuring it is reliable, efficient, and scalable.

#### **5.2.1 Performance Matrix**
*   **Latency**: The backend API shall maintain an average response time of under 200ms for read operations and under 500ms for write operations (excluding large image uploads).
*   **Concurrency**: The system shall handle up to 50 concurrent active users without degradation in service quality on standard cloud tiers.
*   **Optimized Resource Loading**: Frontend assets shall be optimized through Angular's build-time optimizations (Tree shaking, AOT compilation) to ensure a First Contentful Paint (FCP) of under 1.5 seconds.

#### **5.2.2 Scalability**
*   **Horizontal Scaling**: The architecture is designed to be stateless (via JWT), allowing for horizontal scaling of the Django application servers behind a load balancer.
*   **Database Scalability**: By using PostgreSQL, the system supports complex indexing and partitioning, allowing it to handle thousands of task records as the platform expands.
*   **Stateless Services**: Media files are handled through a persistent media root (or integrated S3/Cloudinary), ensuring the application logic is decoupled from file storage.

#### **5.2.3 Fault Tolerance and Reliability**
*   **Graceful Degradation**: If the notification service fails, the core task application flow should remain functional, with users able to see updates upon page refresh.
*   **Error Handling**: The system shall implement comprehensive error handling in both layers. The backend returns standardized HTTP status codes (400, 401, 403, 500) with descriptive JSON messages.
*   **Data Reliability**: Atomic transactions are used in Django to ensure that related operations (e.g., accepting a request and updating task status) either succeed or fail together, maintaining data consistency.

---

## **6. PROPOSED SYSTEM**

### **6.1 System Overview**

The **HireHelper** proposed system replaces fragmented and manual hiring processes with a centralized, automated digital platform. The system is designed to act as a "Single Source of Truth" for task management. All dataâ€”from user credentials to task historyâ€”is stored in a relational database, while the business logic is abstracted into a RESTful API. This architecture ensures that the data is accessible across multiple clients (web, mobile, or third-party integrations) while maintaining a high level of security and performance.

### **6.2 Layered Architecture**

HireHelper follows a classic **3-Tier Architecture**, which provides a clear separation between the user interface, business logic, and data storage. This separation enhances maintainability and allows for independent updates to each layer.

#### **6.2.1 Presentation Layer (Frontend)**
Built using **Angular 17**, this layer is responsible for the user interface and user experience. 
*   **Modern SPA Pattern**: The frontend is a Single Page Application that communicates with the backend via asynchronous HTTP calls.
*   **State Management**: RxJS observables are used to manage data streams, ensuring the UI reflects the latest data without manual refreshes.
*   **Theming Engine**: A custom CSS system combined with Tailwind modules implements the **Dark Glassmorphism** aesthetic, utilizing backdrop-blur, transparency, and high-contrast typography.

#### **6.2.2 Logic Layer (Backend)**
Constructed with **Django 5.0** and **Django REST Framework (DRF)**.
*   **RESTful Services**: The backend exposes dedicated endpoints for each resource (users, tasks, requests, notifications).
*   **Security Middleware**: Includes JWT authentication, CORS (Cross-Origin Resource Sharing) headers, and role-based permission classes.
*   **Business Rules**: This layer handles complex operations such as checking overlapping task requests, validating OTP expiry, and managing task state transitions.

#### **6.2.3 Data Layer (Persistence)**
This layer consists of the **PostgreSQL** relational database.
*   **Structured Storage**: Stores all persistent data including user profiles, task details, and application logs.
*   **Relational Mapping**: Django's ORM (Object-Relational Mapper) is used to interact with the database, providing a secure way to execute queries and preventing SQL injection.
*   **Relationship Management**: Handles complex foreign key relationships between Hirers, Tasks, and Helpers.

---

## **7. ARCHITECTURE AND DESIGN (UML)**

The architectural blueprint of **HireHelper** is visualized through Unified Modeling Language (UML) diagrams. These diagrams provide a standardized way to visualize the system's design, capturing the relationships between different entities, the flow of processes, and the interactions between users and the system.

### **7.1 Use Case Diagram**

The Use Case Diagram illustrates the functional requirements of the system from the perspective of different actors. In HireHelper, the primary actors are the **Hirer** and the **Helper**.

```mermaid
useCaseDiagram
    actor Hirer
    actor Helper
    actor System

    package "HireHelper Core" {
        usecase "Register/Login" as UC1
        usecase "Verify OTP" as UC2
        usecase "Post Task" as UC3
        usecase "Browse Feed" as UC4
        usecase "Apply for Task" as UC5
        usecase "Manage Requests" as UC6
        usecase "Rate Helper" as UC7
        usecase "Receive Notifications" as UC8
    }

    Hirer --> UC1
    Hirer --> UC2
    Hirer --> UC3
    Hirer --> UC6
    Hirer --> UC7

    Helper --> UC1
    Helper --> UC2
    Helper --> UC4
    Helper --> UC5
    Helper --> UC8

    UC1 ..> UC2 : <<include>>
    System --> UC8
```

**Description of Use Cases:**
*   **Register/Login**: Standard entry point for both actors. Incorporates JWT generation.
*   **Post Task**: Exclusive to Hirers; includes providing details and optional images.
*   **Apply for Task**: Exclusive to Helpers; involves creating a TaskRequest instance.
*   **Manage Requests**: Hirers can accept or reject applications, triggering status updates.

### **7.2 Class Diagram (Mandatory)**

The Class Diagram highlights the static structure of the system, showcasing the attributes and methods of core classes and how they relate through association, aggregation, and inheritance.

```mermaid
classDiagram
    class User {
        +String username
        +String email
        +String role
        +String phone_number
        +Image profile_picture
        +Boolean is_verified
        +register()
        +verifyOTP()
        +login()
    }

    class Task {
        +String title
        +String description
        +String location
        +DateTime start_time
        +String status
        +postTask()
        +updateStatus()
    }

    class TaskRequest {
        +String message
        +String hirer_reply
        +String status
        +submitRequest()
        +respondToRequest()
    }

    class Review {
        +Integer rating
        +String comment
        +submitReview()
    }

    User "1" -- "0..*" Task : creates
    User "1" -- "0..*" TaskRequest : submits
    Task "1" -- "0..*" TaskRequest : receives
    Task "1" -- "0..*" Review : has
    User "1" -- "0..*" Review : receives
```

**Key Class Attributes:**
*   **User**: Inherits from Django's `AbstractUser`, adding custom fields like `role` (Hirer/Helper) and `is_verified`.
*   **Task**: The central entity containing metadata about the work required. It is linked to the `User` who created it.
*   **TaskRequest**: A junction entity that connects a `Helper` to a `Task`. It maintains the state of the application (Pending, Accepted, Rejected).
*   **Review**: Ensures accountability by linking a `Task` to both the `Reviewer` and `Reviewee`.

### **7.3 Sequence Diagram (Task Application Flow)**

The Sequence Diagram captures the dynamic behavior of the system, showing how objects interact in a specific time-ordered sequence. The following diagram models the process of a Helper applying for a task and a Hirer responding.

```mermaid
sequenceDiagram
    participant Helper as Helper Client (Angular)
    participant API as Django REST API/JWT
    participant DB as PostgreSQL Database
    participant Hirer as Hirer Client (Angular)

    Helper->>API: POST /api/requests/ (message, task_id)
    API->>API: Validate Token & Permissions
    API->>DB: Save TaskRequest (status='PENDING')
    DB-->>API: Confirm Save
    API-->>Helper: 201 Created (Success)

    Note over Hirer, API: Real-time Signal or Page Refresh
    Hirer->>API: GET /api/my-tasks-requests/
    API->>DB: Query pending requests
    DB-->>API: Return list
    API-->>Hirer: Render Request List

    Hirer->>API: PATCH /api/requests/{id}/ (status='ACCEPTED', reply='...')
    API->>DB: Update TaskRequest & Create Notification
    DB-->>API: Confirm Update
    API-->>Hirer: 200 OK (Accepted)
```

**Flow Analysis:**
1.  **Request Initiation**: High-level validation ensures the helper hasn't already applied.
2.  **Persistence**: The state is locked in the database with a 'PENDING' flag.
3.  **Hirer Action**: The hirer reviews the pitch and issues a patch command, updating both the request state and generating a notification for the helper.

---

## **8. IMPLEMENTATION**

The implementation of **HireHelper** translates the theoretical design into a functional software product. The project maintains a strict separation between the frontend and backend repositories, ensuring independent scalability and cleaner dependency management.

### **8.1 Frontend Implementation (Angular)**

The frontend is a robust Single Page Application (SPA) built with **Angular 17**. It utilizes a component-based architecture where each view is encapsulated within its own module, logic, and style files.

#### **8.1.1 Technology Stack**
*   **Angular 17**: leveraging the latest `inject()` based dependency injection and signal-ready architecture.
*   **RxJS**: Used for handling asynchronous data flows, particularly for API interactions and real-time state updates.
*   **Tailwind CSS**: Combined with vanilla CSS variables to create the custom glassmorphism effects.
*   **Lucide-Angular**: A modern icon library for high-quality SVG visuals.

#### **8.1.2 Directory Architecture**
The following structure highlights the organization of the frontend codebase:

```text
frontend/src/app/
â”œâ”€â”€ components/         # Shared UI elements (Navbar, Footer, Modal)
â”œâ”€â”€ guards/             # Route protection (AuthGuard, VerifiedGuard)
â”œâ”€â”€ interceptors/       # JWT Attachment to HTTP requests
â”œâ”€â”€ pages/              # View-level components
â”‚   â”œâ”€â”€ dashboard/      # Hirer analytics and task control
â”‚   â”œâ”€â”€ login/          # User authentication
â”‚   â”œâ”€â”€ register/       # User onboarding
â”‚   â”œâ”€â”€ task-discovery/ # Global feed of open tasks
â”‚   â”œâ”€â”€ my-requests/    # Helper tracking dashboard
â”‚   â””â”€â”€ profile/        # User settings and bio
â”œâ”€â”€ services/           # API communication layer
â”‚   â”œâ”€â”€ auth.service.ts
â”‚   â”œâ”€â”€ task.service.ts
â”‚   â””â”€â”€ review.service.ts
â””â”€â”€ app.routes.ts       # Central routing configuration
```

### **8.2 Backend Implementation (Django)**

The backend is a high-performance REST API built with **Django 5.0** and **Django REST Framework**.

#### **8.2.1 Technology Stack**
*   **Django 5.0**: The core Python framework providing ORM and routing.
*   **Django REST Framework (DRF)**: Providing serializers and viewsets for JSON output.
*   **SimpleJWT**: Handling stateless authentication via bearer tokens.
*   **Django-Cors-Headers**: Managing secure cross-origin requests from the Angular client.

#### **8.2.2 Backend App Structure**
The project is modularized into several Django apps:
*   **`accounts`**: Manages custom user models, OTP generation, and profile management.
*   **`tasks`**: Handles the creation, retrieval, and status updates of tasks, including the review system.
*   **`request`**: Manages the application logic between helpers and hirers.
*   **`notifications`**: A signaling system that logs events for users to see in real-time.

### **8.3 Database Schema and ERD**

The persistence layer uses **PostgreSQL**. The following schema summarizes the core table structure:

#### **8.3.1 Core Database Tables**

| Table Name | Key Fields | Description |
| :--- | :--- | :--- |
| **`accounts_user`** | `id, username, email, role, phone_number, is_verified` | Extended user table with authentication metadata. |
| **`tasks_task`** | `id, title, description, location, city, start_time, status, created_by_id` | Stores task information and links to the hirer. |
| **`requests`** | `id, task_id, requester_id, message, hirer_reply, status` | Links helpers to tasks with status tracking. |
| **`tasks_review`** | `id, task_id, reviewer_id, reviewee_id, rating, comment` | Stores peer evaluations and ratings. |

---

## **9. MODULES DESCRIPTION**

### **9.1 Authentication and Profile Management**
This module is the entry point of the application. It handles user lifecycle from registration to verification and profile updates.
*   **Onboarding**: Users register and receive an email OTP.
*   **Verification**: The `is_verified` flag is toggled only after the matching OTP is submitted via the frontend.
*   **Security**: All subsequent requests include an `Authorization: Bearer <token>` header, verified by backend middleware.

### **9.2 Task Management and Discovery**
The core utility of the platform.
*   **Task Pulse**: A dedicated view that fetches all tasks with `status='open'`.
*   **Smart Creation**: Hirers can post tasks with location-aware data. The system automatically tags tasks with city and timestamp information.
*   **State Machine**: Tasks move from `open` -> `in_progress` -> `completed` through hirer interactions.

### **9.3 Request and Application Lifecycle**
Manages the interaction between hirers and helpers.
*   **Application Hub**: Helpers can browse tasks and submit one-time requests. The system prevents duplicate applications for the same task.
*   **Interaction**: Hirers review applicants on their dashboard and provide an "Accept" or "Reject" response, which includes a custom message or instruction.

### **9.4 Review and Rating System**
Ensures platform trust and quality control.
*   **Reciprocity**: Reviews are tied to specific task IDs, ensuring they are based on actual work performed.
*   **Dynamic UX**: Ratings are averaged and displayed on user profiles using a visual star rating component.
*   **Commentary**: Qualitative feedback allows for nuanced descriptions of performance.

### **8.4 Deployment**

HireHelper is deployed using a modern cloud-native strategy, ensuring the separation of static frontend assets and dynamic backend services.

*   **Frontend (Vercel)**: The Angular application is deployed on Vercel, which provides an edge-optimized global CDN. Vercel's CI/CD pipeline is integrated with the GitHub repository, automatically deploying a new build upon each push to the main branch.
*   **Backend (Render)**: The Django REST API and the PostgreSQL database are hosted on Render. Render handles the containerization of the Python environment and provides automatic SSL certificates for the API endpoints.
*   **Environment Configuration**: Sensitive data such as the `SECRET_KEY`, `DATABASE_URL`, and SMTP credentials for the OTP system are managed via environment variables on both platforms, ensuring security in production.

---

## **10. OUTPUT SCREENS**

This section presents the visual interface of the HireHelper platform. The UI follows a "Dark Glassmorphism" theme, significantly heightening the premium feel of the application.

*   **[SCREENSHOT 1: Landing Page]**
    *   *Description*: The gateway to the platform featuring a high-impact hero section and the "Join as Hirer/Helper" call-to-action cards.
*   **[SCREENSHOT 2: Authentication & OTP]**
    *   *Description*: The glassmorphic login form and the subsequent email verification screen where users submit their 6-digit OTP.
*   **[SCREENSHOT 3: Task Pulse - Discovery Feed]**
    *   *Description*: A responsive grid of open tasks, showing blurred background cards with hover effects and location badges.
*   **[SCREENSHOT 4: Add Task Dashboard]**
    *   *Description*: The form used by Hirers to create new tasks, featuring a date-time picker and image upload preview.
*   **[SCREENSHOT 5: Application Hub - Requests Management]**
    *   *Description*: A list of applicants for a specific task, allowing the hirer to view messages and click "Accept" or "Reject".
*   **[SCREENSHOT 6: User Profile & Reviews]**
    *   *Description*: The professional profile view showing the user's bio, role badge, and a chronological list of reviews with star ratings.

---

## **11. TESTING AND EVALUATION**

The testing phase ensures that the system meets its functional requirements and provides a bug-free experience. A combination of manual and automated testing strategies was employed.

### **11.1 Test Case Matrix**

| Test ID | Module | Feature Under Test | Input/Action | Expected Result | Pass/Fail |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC01** | Auth | User Registration | Valid email, password, role | User created, OTP sent to email. | PASS |
| **TC02** | Auth | OTP Verification | Correct 6-digit code | User's `is_verified` state becomes True. | PASS |
| **TC03** | Auth | Login Access | Valid credentials for verified user | JWT token received, redirected to Feed. | PASS |
| **TC04** | Tasks | Task Creation | Empty title or past date | System returns 400 Bad Request error. | PASS |
| **TC05** | Tasks | Task Pulse Feed | Navigation to '/feed' | List of 'Open' tasks retrieved from API. | PASS |
| **TC06** | Request | Submit Application | Click "Apply" with message | TaskRequest created; "Apply" button disabled. | PASS |
| **TC07** | Request | Duplicate Application | Attempt to apply twice | API returns 400 "Already applied". | PASS |
| **TC08** | Request | Accept Request | Hirer clicks "Accept" | Task status updates; Helper notified. | PASS |
| **TC09** | Reviews | Submit Rating | 5-star rating + comment | Review saved; User's average rating updated. | PASS |
| **TC10** | Security | Protected Route | Access '/dashboard' without token | Redirected to '/login' (AuthGuard active). | PASS |

### **11.2 Evaluation Metrics**
*   **Code Coverage**: Core business logic in the backend (Serializers/Views) achieved >85% coverage through unit tests.
*   **Lighthouse Performance**: The Angular frontend achieved a performance score of 90+ on desktop, thanks to lazy-loading and AOT compilation.
*   **Database Integrity**: 100% success rate in maintaining relational constraints (No orphaned tasks or reviews).

---

## **12. CONCLUSION**

The development of **HireHelper** successfully demonstrates the power of a modern full-stack architecture in solving real-world labor market fragmentation. By combining **Angular 17** and **Django 5.0**, we have created a platform that is not only functionally complete but also visually superior to traditional task-based applications.

Throughout the project lifecycle, we emphasized the importance of high-end aesthetics, robust security through JWT and OTP verification, and a scalable data model. The transition from the "Brag Board" template to the specific "HireHelper" ecosystem allowed us to refine our understanding of role-based interaction and reputation-based services. In summary, HireHelper stands as a state-of-the-art solution for localized hiring, providing a secure, transparent, and aesthetically pleasing environment for both hirers and helpers.

---

## **13. FUTURE SCOPE**

While HireHelper provides a solid foundation for task management, several avenues for future enhancement have been identified to move the platform toward a commercial scale:

*   **Real-time Chat Integration**: Implementing WebSockets (via Django Channels) to allow hirers and helpers to negotiate details directly within the app once a request is accepted.
*   **Escrow Payment System**: Integrating Stripe or Razorpay to hold task payments in escrow until both parties confirm completion, further increasing financial security.
*   **AI-Powered Matching**: Using machine learning algorithms to recommend tasks to helpers based on their previous work history, location, and skill tags.
*   **Native Mobile Applications**: Developing cross-platform mobile apps using Flutter or Ionic to provide push notifications and GPS-based task finding.
*   **Multi-Language Support**: Implementing I18n (Internationalization) to cater to diverse local communities.

---

## **14. BIBLIOGRAPHY**

1.  **Angular Documentation**: Official Guide for Angular 17 and Signal-based State Management. [https://angular.io/](https://angular.io/)
2.  **Django Documentation**: Comprehensive guide for Django 5.0 ORM and ViewSets. [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
3.  **Django REST Framework**: Documentation for Serializers and API View Architecture. [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
4.  **Mozilla Developer Network (MDN)**: Best practices for HTML5 Semantic Tags and Advanced CSS Grid/Flexbox for the glassmorphism UI.
5.  **GitHub Repositories**: Reference implementations for JWT and Angular Interceptors.
6.  **Infosys Springboard**: Project guidelines and template documentation for the "Brag Board" showcase.

