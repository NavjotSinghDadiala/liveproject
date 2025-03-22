document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const loadMoreBtn = document.getElementById('load-more-btn');
    const jobCount = document.getElementById('job-count');
    const gridViewBtn = document.getElementById('grid-view');
    const listViewBtn = document.getElementById('list-view');
    const jobListings = document.querySelector('.job-listings');
    const locationFilter = document.getElementById('location-filter');
    const industryFilter = document.getElementById('industry-filter');
    const salaryFilter = document.getElementById('salary-filter');
    const jobTypeFilter = document.getElementById('job-type-filter');
    const allSaveButtons = document.querySelectorAll('.save-btn');
    const allApplyButtons = document.querySelectorAll('.apply-btn');
    
    // Sample job data - would come from API in real implementation
    const jobs = [
        {
            id: 1,
            company: "TechCorp",
            position: "Senior UX Designer",
            location: "Remote",
            salary: "$120k-$150k",
            type: "Full-time",
            industry: "tech"
        },
        {
            id: 2,
            company: "WebSolutions Inc.",
            position: "Frontend Developer",
            location: "New York, NY",
            salary: "$90k-$120k",
            type: "Full-time",
            industry: "tech"
        },
        {
            id: 3,
            company: "InnovateCo",
            position: "Product Manager",
            location: "Austin, TX",
            salary: "$100k-$130k",
            type: "Full-time",
            industry: "tech"
        },
        {
            id: 4,
            company: "AnalyticsPlus",
            position: "Data Scientist",
            location: "Boston, MA",
            salary: "$110k-$140k",
            type: "Full-time",
            industry: "tech"
        },
        {
            id: 5,
            company: "GrowthDigital",
            position: "Marketing Specialist",
            location: "Chicago, IL",
            salary: "$70k-$90k",
            type: "Full-time",
            industry: "marketing"
        },
        {
            id: 6,
            company: "CloudTech",
            position: "DevOps Engineer",
            location: "Seattle, WA",
            salary: "$125k-$160k",
            type: "Full-time",
            industry: "tech"
        },
        // More jobs that would be loaded when "Load More" is clicked
        {
            id: 7,
            company: "HealthPlus",
            position: "Nurse Practitioner",
            location: "Miami, FL",
            salary: "$90k-$110k",
            type: "Full-time",
            industry: "healthcare"
        },
        {
            id: 8,
            company: "FinanceGroup",
            position: "Financial Analyst",
            location: "Chicago, IL",
            salary: "$85k-$105k",
            type: "Full-time",
            industry: "finance"
        },
        {
            id: 9,
            company: "EduTech",
            position: "Online Instructor",
            location: "Remote",
            salary: "$60k-$80k",
            type: "Part-time",
            industry: "education"
        },
        {
            id: 10,
            company: "TechGiants",
            position: "Software Engineer",
            location: "San Francisco, CA",
            salary: "$130k-$180k",
            type: "Full-time",
            industry: "tech"
        },
        {
            id: 11,
            company: "MarketingPros",
            position: "SEO Specialist",
            location: "Los Angeles, CA",
            salary: "$75k-$95k",
            type: "Contract",
            industry: "marketing"
        },
        {
            id: 12,
            company: "StartupInc",
            position: "Full Stack Developer",
            location: "Austin, TX",
            salary: "$100k-$130k",
            type: "Full-time",
            industry: "tech"
        }
    ];

    // Track current page and jobs per page
    let currentPage = 1;
    const jobsPerPage = 6;
    let filteredJobs = [...jobs];
    let currentView = 'grid';
    
    // Initialize page
    updateJobCount();
    
    // Event Listeners
    searchBtn.addEventListener('click', performSearch);
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
    
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', loadMoreJobs);
    }
    
    if (gridViewBtn) {
        gridViewBtn.addEventListener('click', function() {
            setViewMode('grid');
        });
    }
    
    if (listViewBtn) {
        listViewBtn.addEventListener('click', function() {
            setViewMode('list');
        });
    }
    
    // Add event listeners to filter dropdowns
    [locationFilter, industryFilter, salaryFilter, jobTypeFilter].forEach(filter => {
        if (filter) {
            filter.addEventListener('change', applyFilters);
        }
    });
    
    // Add event listeners to save buttons
    allSaveButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            toggleSaveJob(e.target);
        });
    });
    
    // Add event listeners to apply buttons
    allApplyButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            applyForJob(e.target);
        });
    });
    
    // Functions
    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        
        filteredJobs = jobs.filter(job => {
            return (
                job.company.toLowerCase().includes(searchTerm) ||
                job.position.toLowerCase().includes(searchTerm) ||
                job.location.toLowerCase().includes(searchTerm)
            );
        });
        
        currentPage = 1;
        renderJobs();
        updateJobCount();
    }
    
    function applyFilters() {
        const locationValue = locationFilter ? locationFilter.value.toLowerCase() : '';
        const industryValue = industryFilter ? industryFilter.value.toLowerCase() : '';
        const salaryValue = salaryFilter ? salaryFilter.value.toLowerCase() : '';
        const jobTypeValue = jobTypeFilter ? jobTypeFilter.value.toLowerCase() : '';
        
        filteredJobs = jobs.filter(job => {
            const locationMatch = !locationValue || job.location.toLowerCase().includes(locationValue);
            const industryMatch = !industryValue || job.industry.toLowerCase() === industryValue;
            const jobTypeMatch = !jobTypeValue || job.type.toLowerCase().includes(jobTypeValue);
            
            // Salary range filtering logic would be more complex in reality
            const salaryMatch = !salaryValue || true; // Placeholder for actual salary range logic
            
            return locationMatch && industryMatch && salaryMatch && jobTypeMatch;
        });
        
        currentPage = 1;
        renderJobs();
        updateJobCount();
    }
    
    function renderJobs() {
        if (!jobListings) return;
        
        // Clear current listings except the "Load More" button
        const loadMoreDiv = document.querySelector('.load-more');
        jobListings.innerHTML = '';
        
        if (loadMoreDiv) {
            jobListings.appendChild(loadMoreDiv);
        }
        
        const startIndex = 0;
        const endIndex = currentPage * jobsPerPage;
        const jobsToShow = filteredJobs.slice(startIndex, endIndex);
        
        // Show message if no jobs found
        if (jobsToShow.length === 0) {
            const noJobsMsg = document.createElement('div');
            noJobsMsg.className = 'no-jobs-message';
            noJobsMsg.textContent = 'No jobs match your search criteria. Try adjusting your filters.';
            jobListings.insertBefore(noJobsMsg, loadMoreDiv);
            loadMoreBtn.style.display = 'none';
            return;
        }
        
        // Create and add job cards
        jobsToShow.forEach(job => {
            const jobCard = createJobCard(job);
            jobListings.insertBefore(jobCard, loadMoreDiv);
        });
        
        // Update Load More button visibility
        if (loadMoreBtn) {
            loadMoreBtn.style.display = endIndex >= filteredJobs.length ? 'none' : 'block';
        }
        
        // Apply current view mode
        setViewMode(currentView, false);
    }
    
    function createJobCard(job) {
        const jobCard = document.createElement('div');
        jobCard.className = 'job-card';
        jobCard.innerHTML = `
            <h3 class="company">${job.company}</h3>
            <h2 class="position"><a href="/job_detail/${job.id}" class="job-title-link">${job.position}</a></h2>
            <div class="job-details">
                <span>${job.location}</span> • <span>${job.salary}</span> • <span>${job.type}</span>
            </div>
            <div class="buttons">
                <button class="apply-btn" data-job-id="${job.id}">Apply Now</button>
                <button class="save-btn" data-job-id="${job.id}">Save</button>
                <a href="/job_detail/${job.id}" class="view-details-btn">View Details</a>
            </div>
        `;
        
        // Add event listeners to new buttons
        const saveBtn = jobCard.querySelector('.save-btn');
        const applyBtn = jobCard.querySelector('.apply-btn');
        
        saveBtn.addEventListener('click', function() {
            toggleSaveJob(saveBtn);
        });
        
        applyBtn.addEventListener('click', function() {
            applyForJob(applyBtn);
        });
        
        return jobCard;
    }
    
    function loadMoreJobs() {
        currentPage++;
        renderJobs();
    }
    
    function updateJobCount() {
        if (jobCount) {
            jobCount.textContent = filteredJobs.length.toLocaleString();
        }
    }
    
    function setViewMode(mode, render = true) {
        currentView = mode;
        
        if (gridViewBtn && listViewBtn) {
            if (mode === 'grid') {
                gridViewBtn.classList.add('active');
                listViewBtn.classList.remove('active');
                jobListings.classList.remove('list-view');
                jobListings.classList.add('grid-view');
            } else {
                listViewBtn.classList.add('active');
                gridViewBtn.classList.remove('active');
                jobListings.classList.remove('grid-view');
                jobListings.classList.add('list-view');
            }
        }
        
        // Add CSS class for styling if not already in styles.css
        if (render) {
            const style = document.createElement('style');
            style.textContent = `
                .job-listings.list-view {
                    display: block !important;
                }
                
                .job-listings.list-view .job-card {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 15px;
                }
                
                .job-listings.list-view .job-card .company,
                .job-listings.list-view .job-card .position,
                .job-listings.list-view .job-card .job-details {
                    margin-bottom: 0;
                }
                
                .job-listings.grid-view {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                    gap: 20px;
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    function toggleSaveJob(button) {
        const jobId = button.getAttribute('data-job-id');
        
        // Toggle saved state
        if (button.classList.contains('saved')) {
            button.classList.remove('saved');
            button.textContent = 'Save';
            
            // In a real app, you would remove from saved jobs in storage
            console.log(`Job ${jobId} removed from saved jobs`);
        } else {
            button.classList.add('saved');
            button.textContent = 'Saved';
            button.style.backgroundColor = '#ffde59';
            
            // In a real app, you would add to saved jobs in storage
            console.log(`Job ${jobId} added to saved jobs`);
        }
    }
    
    function applyForJob(button) {
        const jobId = button.getAttribute('data-job-id');
        const jobPosition = button.closest('.job-card').querySelector('.position').textContent;
        
        // In a real app, this would redirect to application form
        alert(`Applying for ${jobPosition}. In a complete application, you would be redirected to the application form.`);
        console.log(`User applied for job ${jobId}`);
    }
    
    // Mobile menu toggle (assuming there would be a mobile menu button)
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }
    
    // Intersection Observer for lazy loading jobs when scrolling
    if ('IntersectionObserver' in window && loadMoreBtn) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && loadMoreBtn.style.display !== 'none') {
                    loadMoreJobs();
                }
            });
        }, {
            rootMargin: '0px 0px 200px 0px'
        });
        
        observer.observe(loadMoreBtn);
    }
});