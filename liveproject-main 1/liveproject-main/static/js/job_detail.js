// Job Data (Can be replaced with API data later)
const jobDetails = {
    title: "Senior UX Designer",
    company: "TechCorp",
    location: "San Francisco, CA • Remote",
    salary: "$120K-$150K",
    jobType: "Full-time",
    postedTime: "Posted 2 days ago",
    applicationDeadline: "Application Deadline: 30 days",
    description: "TechCorp is seeking a Senior UX Designer to join our product team. In this role, you will lead the design of innovative digital experiences that delight our users and drive business growth. You'll collaborate with cross-functional teams to translate complex requirements into intuitive interfaces.",
    responsibilities: [
        "Lead UX design for key product initiatives",
        "Create wireframes, prototypes, and high-fidelity designs",
        "Conduct user research and usability testing",
        "Collaborate with product managers and engineers",
        "Mentor junior designers and contribute to design system"
    ],
    requirements: [
        "5+ years of UX design experience",
        "Strong portfolio demonstrating user-centered design",
        "Proficiency in Figma, Sketch, and prototyping tools",
        "Experience with user research methodologies",
        "Excellent communication and collaboration skills"
    ],
    benefits: [
        "Competitive salary and equity package",
        "Comprehensive health, dental, and vision insurance",
        "Flexible remote work policy",
        "Professional development budget",
        "Generous PTO and parental leave"
    ],
    companyInfo: {
        name: "TechCorp",
        description: "TechCorp is a leading technology company specializing in innovative software solutions. With over 500 employees worldwide, we're on a mission to transform how people interact with technology. Our inclusive culture encourages creativity and continuous learning."
    },
    similarJobs: [
        {
            company: "DesignHub",
            title: "UX/UI Designer",
            location: "New York, NY",
            salary: "$115K-$140K",
            workType: "Remote"
        },
        {
            company: "CreativeTech",
            title: "Product Designer",
            location: "Austin, TX",
            salary: "$115K-$145K",
            workType: "Hybrid"
        }
    ]
};

// Function to Populate Job Data
function populateJobDetails() {
    // Get job_id from URL if available
    const urlParams = new URLSearchParams(window.location.search);
    const jobIdFromUrl = window.location.pathname.split('/').pop();
    
    // For demo purposes, we're using the static job data
    // In a real application, you would fetch the job details from an API using the job_id
    console.log("Job ID from URL:", jobIdFromUrl);
    
    document.getElementById("job-title").innerText = jobDetails.title;
    document.getElementById("job-title-nav").innerText = jobDetails.title;
    document.getElementById("company-name").innerText = jobDetails.company;
    document.getElementById("location-text").innerText = jobDetails.location;
    document.getElementById("salary").innerText = jobDetails.salary;
    document.getElementById("job-type").innerText = jobDetails.jobType;
    document.getElementById("posted-time").innerText = jobDetails.postedTime;
    document.getElementById("application-deadline").innerText = jobDetails.applicationDeadline;
    document.getElementById("job-description").innerText = jobDetails.description;
    document.getElementById("company-info-name").innerText = jobDetails.companyInfo.name;
    document.getElementById("company-info-description").innerText = jobDetails.companyInfo.description;

    // Populate Responsibilities
    const responsibilitiesList = document.getElementById("responsibilities-list");
    jobDetails.responsibilities.forEach(responsibility => {
        const li = document.createElement("li");
        li.innerText = responsibility;
        responsibilitiesList.appendChild(li);
    });

    // Populate Requirements
    const requirementsList = document.getElementById("requirements-list");
    jobDetails.requirements.forEach(requirement => {
        const li = document.createElement("li");
        li.innerText = requirement;
        requirementsList.appendChild(li);
    });

    // Populate Benefits
    const benefitsList = document.getElementById("benefits-list");
    jobDetails.benefits.forEach(benefit => {
        const li = document.createElement("li");
        li.innerText = benefit;
        benefitsList.appendChild(li);
    });

    // Populate Similar Jobs
    const similarJobsContainer = document.getElementById("similar-jobs");
    jobDetails.similarJobs.forEach(job => {
        const jobDiv = document.createElement("div");
        jobDiv.classList.add("similar-job");
        jobDiv.innerHTML = `
            <h4><i class="fas fa-building"></i> ${job.company}</h4>
            <p><i class="fas fa-briefcase"></i> ${job.title}</p>
            <p><i class="fas fa-map-marker-alt"></i> ${job.location} | <i class="fas fa-money-bill-wave"></i> ${job.salary} | <i class="fas fa-user-clock"></i> ${job.workType}</p>
            <button><i class="fas fa-eye"></i> View Job</button>
        `;
        similarJobsContainer.appendChild(jobDiv);
    });
    
    // Check for saved mode preference
    if (localStorage.getItem("mode") === "light") {
        document.body.classList.add("light-mode");
        document.querySelector(".toggle-mode").textContent = "Dark Mode";
    }
}

// Toggle between dark and light mode
function toggleMode() {
    document.body.classList.toggle("light-mode");
    
    // Update button text
    const button = document.querySelector(".toggle-mode");
    if (document.body.classList.contains("light-mode")) {
        button.textContent = "Dark Mode";
        // Save preference
        localStorage.setItem("mode", "light");
    } else {
        button.textContent = "Light Mode";
        // Save preference
        localStorage.setItem("mode", "dark");
    }
}

// Check for saved mode preference
document.addEventListener("DOMContentLoaded", function() {
    // Check for saved mode preference
    if (localStorage.getItem("mode") === "light") {
        document.body.classList.add("light-mode");
        document.querySelector(".toggle-mode").textContent = "Dark Mode";
    }
    
    // Initialize job details
    populateJobDetails();
}); 