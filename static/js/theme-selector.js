// AFL Team Theme Selector
const aflTeams = {
    'adelaide': {
        name: 'Adelaide Crows',
        primary: '#E21937',
        secondary: '#002B5C',
        accent: '#FFD200'
    },
    'brisbane': {
        name: 'Brisbane Lions',
        primary: '#A30046',
        secondary: '#0055A3',
        accent: '#FDBE57'
    },
    'carlton': {
        name: 'Carlton Blues',
        primary: '#021A31',
        secondary: '#FFFFFF',
        accent: '#87CEEB'
    },
    'collingwood': {
        name: 'Collingwood Magpies',
        primary: '#000000',
        secondary: '#FFFFFF',
        accent: '#CCCCCC'
    },
    'essendon': {
        name: 'Essendon Bombers',
        primary: '#FF1100',
        secondary: '#000000',
        accent: '#FFFFFF'
    },
    'fremantle': {
        name: 'Fremantle Dockers',
        primary: '#1D1196',
        secondary: '#FFFFFF',
        accent: '#E6E6FA'
    },
    'geelong': {
        name: 'Geelong Cats',
        primary: '#05173F',
        secondary: '#FFFFFF',
        accent: '#87CEEB'
    },
    'goldcoast': {
        name: 'Gold Coast Suns',
        primary: '#FC1921',
        secondary: '#FFE831',
        accent: '#095AA5'
    },
    'gws': {
        name: 'GWS Giants',
        primary: '#F78F1E',
        secondary: '#545874',
        accent: '#FFFFFF'
    },
    'hawthorn': {
        name: 'Hawthorn Hawks',
        primary: '#361500',
        secondary: '#FFB300',
        accent: '#FFFFFF'
    },
    'melbourne': {
        name: 'Melbourne Demons',
        primary: '#0F1131',
        secondary: '#CC2031',
        accent: '#FFFFFF'
    },
    'northmelbourne': {
        name: 'North Melbourne Kangaroos',
        primary: '#0E2B8D',
        secondary: '#FFFFFF',
        accent: '#87CEEB'
    },
    'portadelaide': {
        name: 'Port Adelaide Power',
        primary: '#008E8F',
        secondary: '#000000',
        accent: '#FFFFFF'
    },
    'richmond': {
        name: 'Richmond Tigers',
        primary: '#FFD600',
        secondary: '#000000',
        accent: '#FFFFFF'
    },
    'stkilda': {
        name: 'St Kilda Saints',
        primary: '#FC1921',
        secondary: '#000000',
        accent: '#FFFFFF'
    },
    'sydney': {
        name: 'Sydney Swans',
        primary: '#F20E17',
        secondary: '#FFFFFF',
        accent: '#FFB6C1'
    },
    'westcoast': {
        name: 'West Coast Eagles',
        primary: '#05173F',
        secondary: '#FFC211',
        accent: '#FFFFFF'
    },
    'westernbulldogs': {
        name: 'Western Bulldogs',
        primary: '#0D3652',
        secondary: '#F20E17',
        accent: '#FFFFFF'
    }
};

// Initialize theme selector on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeThemeSelector();
    loadSavedTheme();
});

function initializeThemeSelector() {
    const container = document.getElementById('teamThemeSelector');
    if (!container) return;

    container.innerHTML = '';
    
    Object.keys(aflTeams).forEach(teamKey => {
        const team = aflTeams[teamKey];
        const teamButton = createTeamButton(teamKey, team);
        container.appendChild(teamButton);
    });
}

function createTeamButton(teamKey, team) {
    const col = document.createElement('div');
    col.className = 'col-6 col-md-4 col-lg-3';
    
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'btn w-100 team-theme-btn';
    button.onclick = () => applyTeamTheme(teamKey);
    button.setAttribute('data-team', teamKey);
    
    // Create gradient background
    button.style.background = `linear-gradient(135deg, ${team.primary} 0%, ${team.secondary} 100%)`;
    button.style.border = `2px solid ${team.accent}`;
    button.style.color = getContrastColor(team.primary);
    button.style.transition = 'all 0.3s ease';
    
    // Team name and colors indicator
    button.innerHTML = `
        <div class="text-center py-2">
            <div class="fw-bold small">${team.name}</div>
            <div class="d-flex justify-content-center mt-1">
                <span class="color-indicator me-1" style="background-color: ${team.primary}"></span>
                <span class="color-indicator me-1" style="background-color: ${team.secondary}"></span>
                <span class="color-indicator" style="background-color: ${team.accent}"></span>
            </div>
        </div>
    `;
    
    // Hover effects
    button.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.05)';
        this.style.boxShadow = `0 4px 12px rgba(0,0,0,0.2)`;
    });
    
    button.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
        this.style.boxShadow = 'none';
    });
    
    col.appendChild(button);
    return col;
}

function applyTeamTheme(teamKey) {
    const team = aflTeams[teamKey];
    if (!team) return;
    
    // Apply CSS custom properties for theming
    const root = document.documentElement;
    
    // Update Bootstrap color variables
    root.style.setProperty('--bs-primary', team.primary);
    root.style.setProperty('--bs-primary-rgb', hexToRgb(team.primary));
    root.style.setProperty('--bs-secondary', team.secondary);
    root.style.setProperty('--bs-secondary-rgb', hexToRgb(team.secondary));
    root.style.setProperty('--bs-info', team.accent);
    root.style.setProperty('--bs-info-rgb', hexToRgb(team.accent));
    
    // Custom theme variables
    root.style.setProperty('--team-primary', team.primary);
    root.style.setProperty('--team-secondary', team.secondary);
    root.style.setProperty('--team-accent', team.accent);
    
    // Update active state
    document.querySelectorAll('.team-theme-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const activeButton = document.querySelector(`[data-team="${teamKey}"]`);
    if (activeButton) {
        activeButton.classList.add('active');
        activeButton.style.transform = 'scale(0.95)';
        setTimeout(() => {
            activeButton.style.transform = 'scale(1)';
        }, 150);
    }
    
    // Save theme preference
    localStorage.setItem('aflTheme', teamKey);
    
    // Show success message
    showThemeMessage(`${team.name} theme applied!`);
}

function resetTheme() {
    const root = document.documentElement;
    
    // Reset to original Bootstrap values
    root.style.removeProperty('--bs-primary');
    root.style.removeProperty('--bs-primary-rgb');
    root.style.removeProperty('--bs-secondary');
    root.style.removeProperty('--bs-secondary-rgb');
    root.style.removeProperty('--bs-info');
    root.style.removeProperty('--bs-info-rgb');
    root.style.removeProperty('--team-primary');
    root.style.removeProperty('--team-secondary');
    root.style.removeProperty('--team-accent');
    
    // Remove active states
    document.querySelectorAll('.team-theme-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Clear saved preference
    localStorage.removeItem('aflTheme');
    
    showThemeMessage('Default theme restored!');
}

function loadSavedTheme() {
    const savedTheme = localStorage.getItem('aflTheme');
    if (savedTheme && aflTeams[savedTheme]) {
        applyTeamTheme(savedTheme);
    }
}

function getContrastColor(hex) {
    // Convert hex to RGB
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    
    // Calculate luminance
    const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
    
    return luminance > 0.5 ? '#000000' : '#FFFFFF';
}

function hexToRgb(hex) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `${r}, ${g}, ${b}`;
}

function showThemeMessage(message) {
    // Create and show a toast message
    const toast = document.createElement('div');
    toast.className = 'alert alert-success alert-dismissible fade show position-fixed';
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 250px;';
    toast.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 3000);
}