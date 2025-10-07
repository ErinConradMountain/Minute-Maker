# Minute Maker - User Interface Definition

## Overview
The Minute Maker web application provides an intuitive, step-by-step interface for converting meeting recordings into professional meeting minutes. The UI emphasizes simplicity, visual feedback, and professional appearance while guiding users through the transcription and minute generation process.

## Core Application Flow
1. **Audio Upload** → 2. **Transcription** → 3. **AI Processing** → 4. **Review & Edit** → 5. **Export**

## Visual Design Philosophy
- **Clean & Professional**: Minimal design with plenty of whitespace
- **Progress-Oriented**: Clear visual indicators showing current step and overall progress
- **Responsive**: Works seamlessly on desktop, tablet, and mobile devices
- **Accessible**: High contrast, screen reader friendly, keyboard navigation
- **Modern**: Contemporary web design with subtle animations and micro-interactions

---

## Main Interface Layout

### Header Section
```
┌─────────────────────────────────────────────────────────────┐
│  🎙️ Minute Maker                            [Settings] [Help] │
│  Transform your meetings into professional minutes           │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
- Application logo and name
- Tagline/subtitle
- Settings dropdown (API keys, preferences)
- Help/documentation link
- Optional user account indicator

### Progress Indicator
```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Upload → Step 2: Transcribe → Step 3: Generate → Step 4: Review → Step 5: Export │
│ ●━━━━━━━━━━○━━━━━━━━━━○━━━━━━━━━━○━━━━━━━━━━○                │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Visual progress bar with 5 distinct steps
- Current step highlighted
- Completed steps marked with checkmarks
- Remaining steps shown as inactive

### Main Content Area
Large, centered workspace that adapts based on current step. Content changes dynamically while maintaining consistent layout structure.

---

## Step-by-Step Interface Definitions

### Step 1: Audio Upload Interface

#### Upload Zone (Primary Focus)
```
┌─────────────────────────────────────────────────────────────┐
│                    📁 Upload Audio File                     │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │         🎵 Drag & Drop Audio File Here             │   │
│  │                     or                              │   │
│  │             [Choose File] button                    │   │
│  │                                                     │   │
│  │    Supported: MP3, WAV, M4A, FLAC (Max: 25MB)     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Interactive Elements:**
- Drag-and-drop zone with hover effects
- File picker button
- File format validation with visual feedback
- File size indicator and limits
- Preview of selected file (name, size, duration if possible)

#### Additional Options Panel
```
┌─────────────────────────────────────────────────────────────┐
│ ⚙️ Transcription Options                                    │
│ ┌─────────────────────────────────────────────────────┐     │
│ │ Language: [English ▼]                               │     │
│ │ Quality:  ○ Standard  ●High Quality (slower)        │     │
│ │ Speaker:  ☑ Identify multiple speakers              │     │
│ └─────────────────────────────────────────────────────┘     │
│                                                             │
│               [Cancel] [Start Transcription]                │
└─────────────────────────────────────────────────────────────┘
```

### Step 2: Transcription in Progress

#### Loading Interface
```
┌─────────────────────────────────────────────────────────────┐
│                  🎙️ Transcribing Audio...                  │
│                                                             │
│              ████████████████████████████                  │
│                        67%                                 │
│                                                             │
│  📝 Converting speech to text using AI-powered recognition │
│     Estimated time remaining: 2 minutes 15 seconds         │
│                                                             │
│     File: meeting_recording.mp3 (15.2 MB)                 │
│     Duration: 45 minutes                                    │
│                                                             │
│                    [Cancel Process]                         │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Animated progress bar with percentage
- Real-time status updates
- Time estimates
- File information display
- Option to cancel operation

### Step 3: AI Processing Interface

#### Processing Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│                🧠 Generating Meeting Minutes...             │
│                                                             │
│  ✅ Abstract Summary          ████████████████████ 100%    │
│  🔄 Key Points Extraction     ████████████████░░░░ 80%     │
│  ⏳ Action Items Analysis     ████████░░░░░░░░░░░░ 40%     │
│  ⏳ Sentiment Analysis        ░░░░░░░░░░░░░░░░░░░░ 0%      │
│                                                             │
│  💭 Current: Analyzing key discussion points...             │
│     Using Qwen AI for intelligent content extraction       │
│                                                             │
│                    [View Transcript]                        │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Individual progress for each AI task
- Current operation description
- Option to preview transcript
- Visual indicators for completed/in-progress/pending tasks

### Step 4: Review & Edit Interface

#### Split-Panel Layout
```
┌─────────────────────────────────────────────────────────────┐
│ 📋 Meeting Minutes Review                 [Save Draft] [Export] │
├─────────────────────────┬───────────────────────────────────┤
│ SECTIONS                │ CONTENT EDITOR                    │
│                         │                                   │
│ 📄 Abstract Summary     │ ┌─────────────────────────────┐   │
│ 🎯 Key Points          │ │ The team discussed Q4       │   │
│ ✅ Action Items        │ │ objectives and budget       │   │
│ 😊 Sentiment           │ │ allocation. Key decisions   │   │
│                         │ │ include...                  │   │
│ [+ Add Section]         │ │                             │   │
│                         │ │ [Edit Mode] [Preview]       │   │
│                         │ └─────────────────────────────┘   │
│                         │                                   │
│ TRANSCRIPT              │ METADATA                          │
│ [Show/Hide]            │ ┌─────────────────────────────┐   │
│                         │ │ Meeting Date: [Date Picker] │   │
│                         │ │ Duration: 45:32             │   │
│                         │ │ Attendees: [Text Field]     │   │
│                         │ │ Meeting Type: [Dropdown]    │   │
│                         │ └─────────────────────────────┘   │
└─────────────────────────┴───────────────────────────────────┘
```

**Interactive Features:**
- Expandable/collapsible sections
- Rich text editor for each section
- Real-time preview mode
- Drag-and-drop section reordering
- Add custom sections
- Meeting metadata form
- Access to original transcript

#### Section-Specific Editors

**Abstract Summary Editor:**
```
┌─────────────────────────────────────────────────────────────┐
│ 📄 Abstract Summary                                [↑] [↓] [×]│
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ The marketing team convened to discuss Q4 campaign     │ │
│ │ strategies and budget allocation. Key decisions        │ │
│ │ include launching three major initiatives...           │ │
│ │                                                         │ │
│ │ [Suggested improvements: Make more concise]            │ │
│ └─────────────────────────────────────────────────────────┘ │
│ Word count: 127 | [Regenerate with AI] [Expand] [Compress] │
└─────────────────────────────────────────────────────────────┘
```

**Action Items Editor:**
```
┌─────────────────────────────────────────────────────────────┐
│ ✅ Action Items                                   [↑] [↓] [×]│
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ • Sarah: Create Q4 budget proposal - Due: Oct 15       │ │
│ │ • Mike: Research competitor pricing - Due: Oct 12      │ │
│ │ • Team: Review campaign mockups - Due: Oct 20          │ │
│ │                                                         │ │
│ │ [+ Add Action Item]                                     │ │
│ └─────────────────────────────────────────────────────────┘ │
│ 3 items | [Sort by Date] [Sort by Person] [Export to Calendar] │
└─────────────────────────────────────────────────────────────┘
```

### Step 5: Export Interface

#### Export Options Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│                    📤 Export Meeting Minutes                │
│                                                             │
│ FORMAT OPTIONS:                                             │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│ │ 📄 Word Doc │ │ 📋 PDF File │ │ 🌐 HTML     │           │
│ │             │ │             │ │             │           │
│ │ [Download]  │ │ [Download]  │ │ [Download]  │           │
│ └─────────────┘ └─────────────┘ └─────────────┘           │
│                                                             │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│ │ 📧 Email    │ │ 📱 Send to  │ │ ☁️ Cloud    │           │
│ │             │ │    Teams    │ │   Storage   │           │
│ │ [Send]      │ │ [Share]     │ │ [Save]      │           │
│ └─────────────┘ └─────────────┘ └─────────────┘           │
│                                                             │
│ TEMPLATE OPTIONS:                                           │
│ ○ Professional   ○ Executive Summary   ○ Detailed          │
│ ○ Action-Focused ○ Custom Template                         │
│                                                             │
│               [Preview] [Start New Meeting]                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Additional UI Components

### Settings Modal
```
┌─────────────────────────────────────────────────────────────┐
│ ⚙️ Settings                                            [×]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ API CONFIGURATION:                                          │
│ OpenAI API Key:     [•••••••••••••••••••••] [Test]         │
│ OpenRouter API Key: [•••••••••••••••••••••] [Test]         │
│                                                             │
│ DEFAULT PREFERENCES:                                        │
│ Language:           [English ▼]                            │
│ AI Model:           [Qwen-1.5-72B ▼]                       │
│ Export Format:      [Word Document ▼]                      │
│ Auto-save drafts:   [☑]                                    │
│                                                             │
│ MEETING DEFAULTS:                                           │
│ Company Name:       [________________________]              │
│ Default Attendees:  [________________________]              │
│ Meeting Types:      [________________________]              │
│                                                             │
│                     [Cancel] [Save Settings]               │
└─────────────────────────────────────────────────────────────┘
```

### Help & Documentation Sidebar
```
┌─────────────────────────────────────────────────────────────┐
│ ❓ Help & Tips                                         [×]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 🎯 QUICK START:                                             │
│ 1. Upload your meeting recording                            │
│ 2. Wait for transcription                                   │
│ 3. Review AI-generated minutes                              │
│ 4. Export in your preferred format                          │
│                                                             │
│ 💡 TIPS FOR BEST RESULTS:                                   │
│ • Use clear audio recordings                                │
│ • Ensure speakers are audible                               │
│ • Limit background noise                                    │
│ • Keep files under 25MB                                     │
│                                                             │
│ 🔧 TROUBLESHOOTING:                                         │
│ • Check API key configuration                               │
│ • Verify internet connection                                │
│ • Try different audio formats                               │
│                                                             │
│ 📚 [Full Documentation] [Video Tutorials] [Contact Support] │
└─────────────────────────────────────────────────────────────┘
```

---

## Responsive Design Considerations

### Mobile Layout (< 768px)
- Single-column layout
- Collapsible sections
- Touch-friendly buttons (minimum 44px)
- Simplified upload interface
- Swipe navigation between steps

### Tablet Layout (768px - 1024px)
- Adapted two-column layout for review step
- Larger touch targets
- Optimized for both portrait and landscape

### Desktop Layout (> 1024px)
- Full multi-column layouts
- Hover effects and tooltips
- Keyboard shortcuts
- Drag-and-drop functionality

---

## Technical Implementation Notes

### Frontend Technologies
- **HTML5**: Semantic markup, audio element for playback
- **CSS3**: Flexbox/Grid layouts, CSS animations, responsive design
- **JavaScript (ES6+)**: File handling, AJAX requests, real-time updates
- **Optional Framework**: Vue.js or React for component-based architecture

### Key JavaScript Functionality
```javascript
// File upload handling
const handleFileUpload = (file) => {
  validateFile(file);
  updateProgressBar();
  sendToBackend(file);
};

// Real-time progress updates
const updateProgress = (step, percentage) => {
  updateProgressBar(step, percentage);
  updateStatusMessage(step);
};

// Dynamic content loading
const loadStepContent = (stepNumber) => {
  showSpinner();
  fetchStepData(stepNumber)
    .then(renderContent)
    .finally(hideSpinner);
};
```

### API Integration Points
- `/upload` - File upload endpoint
- `/transcribe` - Transcription status and results
- `/generate-minutes` - AI processing status
- `/export` - Document generation and download

### Accessibility Features
- ARIA labels and roles
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode support
- Focus management between steps

---

## Visual Design Elements

### Color Palette
- **Primary**: #2563EB (Blue) - Progress, actions
- **Secondary**: #059669 (Green) - Success states
- **Accent**: #DC2626 (Red) - Errors, warnings
- **Neutral**: #64748B (Gray) - Text, borders
- **Background**: #F8FAFC (Light Gray) - Page background

### Typography
- **Headings**: Inter or system fonts, weights 600-700
- **Body Text**: Inter or system fonts, weight 400
- **Monospace**: JetBrains Mono for code/file names

### Icons & Illustrations
- Consistent icon set (Heroicons or Lucide)
- Custom illustrations for empty states
- Loading animations for processing states

### Animations
- Smooth page transitions (300ms ease-in-out)
- Progress bar animations
- Hover effects on interactive elements
- Loading spinners and skeleton screens

This UI definition provides a comprehensive blueprint for creating an intuitive, professional, and feature-rich web interface for the Minute Maker application.