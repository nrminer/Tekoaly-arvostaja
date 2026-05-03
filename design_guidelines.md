{
  "product": {
    "name": "Finnish CV Reviewer",
    "type": "hybrid_fullstack_saas_ai_review_tool",
    "audience": [
      "Job seekers applying in Finland",
      "International applicants needing Finnish-market alignment",
      "Career changers tailoring CVs to specific roles"
    ],
    "success_actions": [
      "Upload PDF/DOCX or paste CV text",
      "Optionally add target job title/industry/job description",
      "Run AI review and receive section-by-section scored report",
      "Copy STAR rewrite examples",
      "Save and reopen recent reviews"
    ]
  },
  "visual_personality": {
    "brand_attributes": [
      "trustworthy",
      "calm Nordic clarity",
      "editorial precision",
      "supportive coaching (not judgmental)"
    ],
    "style_fusion": {
      "layout_principle": "Swiss/Editorial dashboard (clear typographic hierarchy + generous whitespace)",
      "surface_style": "Soft minimalism with subtle borders + light noise texture (no glassy transparency)",
      "accent_behavior": "Teal/seafoam accents for actions + progress; warm sand for highlights"
    },
    "do_not": [
      "Do not use purple (AI chat restriction)",
      "Do not use centered reading layouts for long text",
      "Do not use heavy gradients or gradient text",
      "Do not use transparent backgrounds"
    ]
  },
  "inspiration_refs": {
    "search_notes": [
      "Look at Dribbble: clean dashboard / editorial dashboard / resume review",
      "Behance: file upload UI / report UI",
      "Finnish CV guidance: InfoFinland + VisualCV Finland resume"
    ],
    "urls": [
      {
        "label": "Dribbble clean dashboard tag",
        "url": "https://dribbble.com/tags/clean-dashboard"
      },
      {
        "label": "Dribbble editorial dashboard search",
        "url": "https://dribbble.com/search/editorial-dashboard"
      },
      {
        "label": "Behance uploading UI design search",
        "url": "https://www.behance.net/search/projects/uploading%20ui%20design"
      },
      {
        "label": "InfoFinland: job application and CV",
        "url": "https://infofinland.fi/work-and-enterprise/find-a-job-in-finland/job-application-and-cv"
      },
      {
        "label": "VisualCV: Finland resume",
        "url": "https://www.visualcv.com/international/finland-resume/"
      }
    ]
  },
  "design_tokens": {
    "fonts": {
      "google_fonts_import": [
        "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Figtree:wght@400;500;600&display=swap"
      ],
      "usage": {
        "heading": "Space Grotesk",
        "body": "Figtree",
        "mono": "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace"
      }
    },
    "typography_scale_tailwind": {
      "h1": "text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight",
      "h2": "text-base md:text-lg font-medium text-muted-foreground",
      "h3": "text-lg font-semibold",
      "body": "text-sm md:text-base",
      "small": "text-xs text-muted-foreground"
    },
    "color_system": {
      "notes": [
        "Aim: Nordic calm + high readability",
        "Use teal as primary action color; keep backgrounds off-white",
        "Gradients only as subtle hero backdrop accent (<20% viewport)"
      ],
      "css_custom_properties": {
        "light": {
          "--background": "180 20% 99%",
          "--foreground": "222 47% 11%",
          "--card": "0 0% 100%",
          "--card-foreground": "222 47% 11%",
          "--popover": "0 0% 100%",
          "--popover-foreground": "222 47% 11%",
          "--primary": "173 80% 26%",
          "--primary-foreground": "0 0% 100%",
          "--secondary": "210 20% 96%",
          "--secondary-foreground": "222 47% 11%",
          "--muted": "210 20% 96%",
          "--muted-foreground": "215 16% 47%",
          "--accent": "174 45% 92%",
          "--accent-foreground": "173 80% 18%",
          "--destructive": "0 72% 51%",
          "--destructive-foreground": "0 0% 100%",
          "--border": "214 20% 90%",
          "--input": "214 20% 90%",
          "--ring": "173 80% 26%",
          "--radius": "0.75rem",
          "--shadow-color": "222 47% 11%",
          "--shadow-soft": "0 10px 30px hsl(var(--shadow-color) / 0.08)",
          "--shadow-lift": "0 18px 50px hsl(var(--shadow-color) / 0.12)",
          "--focus": "0 0 0 3px hsl(173 80% 26% / 0.25)",
          "--success": "160 84% 30%",
          "--warning": "38 92% 50%",
          "--info": "199 89% 48%"
        }
      },
      "palette_hex_reference": {
        "ink": "#0B1220",
        "slate": "#334155",
        "border": "#E2E8F0",
        "paper": "#FFFFFF",
        "fog": "#F7FAFA",
        "teal_primary": "#0F766E",
        "teal_hover": "#115E59",
        "seafoam": "#99F6E4",
        "sand": "#F4EDE2",
        "danger": "#DC2626"
      },
      "allowed_gradient_usage": {
        "hero_backdrop_only": "bg-[radial-gradient(1200px_circle_at_20%_10%,rgba(153,246,228,0.35),transparent_55%),radial-gradient(900px_circle_at_80%_0%,rgba(244,237,226,0.45),transparent_50%)]",
        "rule": "Keep gradient overlays decorative and behind content; never on cards or text blocks"
      }
    },
    "spacing": {
      "layout": {
        "page_padding": "px-4 sm:px-6 lg:px-10",
        "section_spacing": "py-10 sm:py-14",
        "card_padding": "p-4 sm:p-6",
        "gap": "gap-4 sm:gap-6"
      }
    },
    "radii_and_borders": {
      "radius": {
        "card": "rounded-xl",
        "button": "rounded-lg",
        "input": "rounded-lg"
      },
      "borders": {
        "default": "border border-border",
        "subtle": "border border-border/70"
      }
    }
  },
  "layout_and_information_architecture": {
    "global_shell": {
      "structure": "Single-page app with top nav + main content + optional right-side history panel on desktop",
      "grid": {
        "desktop": "max-w-6xl mx-auto grid grid-cols-12 gap-6",
        "main_column": "col-span-12 lg:col-span-8",
        "side_column": "hidden lg:block lg:col-span-4"
      },
      "reading_width": "For long report text, constrain to max-w-prose inside cards (not centered page-wide)."
    },
    "sections": [
      {
        "id": "hero",
        "purpose": "Explain value + set trust + show privacy note",
        "layout": "Left: headline + subhead + trust bullets; Right: compact 'Start review' card (on desktop). On mobile: stack with CTA card below.",
        "key_elements": [
          "Primary CTA: Start review",
          "Secondary: View example report (opens dialog)",
          "Trust row: 'Finnish-market aligned', 'Privacy-first', 'Actionable rewrites'"
        ]
      },
      {
        "id": "submission_panel",
        "purpose": "Upload/paste CV + optional context",
        "layout": "Tabbed: Upload file / Paste text. Below: optional fields (job title, industry, job description).",
        "key_elements": [
          "Drag-and-drop zone with file type hints",
          "File preview row (name, size, remove)",
          "Optional context collapsible",
          "Submit button with progress"
        ]
      },
      {
        "id": "analysis_state",
        "purpose": "Show progress + keep user calm",
        "layout": "Inline progress card with steps list + skeleton placeholders for report sections.",
        "key_elements": [
          "Progress bar",
          "Step list: Extracting text → Checking structure → Scoring sections → Drafting rewrites → Finalizing",
          "Cancel button (if supported)"
        ]
      },
      {
        "id": "results_report",
        "purpose": "Deliver structured feedback with scores and actions",
        "layout": "Top summary row (overall score + key strengths + top fixes). Then accordion per section with score badge + issues + recommendations + examples.",
        "key_elements": [
          "Overall score card",
          "Section scorecards",
          "Accordion sections",
          "Copy buttons for rewrite examples",
          "Resource links (Finland-specific)"
        ]
      },
      {
        "id": "history_panel",
        "purpose": "Reopen recent reviews",
        "layout": "Right sidebar list with search + filters; on mobile becomes Drawer/Sheet.",
        "key_elements": [
          "Search input",
          "List items with date + target role",
          "Reopen action",
          "Delete action with confirm dialog"
        ]
      }
    ]
  },
  "component_path": {
    "shadcn_primary": [
      "/app/frontend/src/components/ui/button.jsx",
      "/app/frontend/src/components/ui/card.jsx",
      "/app/frontend/src/components/ui/input.jsx",
      "/app/frontend/src/components/ui/textarea.jsx",
      "/app/frontend/src/components/ui/label.jsx",
      "/app/frontend/src/components/ui/tabs.jsx",
      "/app/frontend/src/components/ui/progress.jsx",
      "/app/frontend/src/components/ui/accordion.jsx",
      "/app/frontend/src/components/ui/badge.jsx",
      "/app/frontend/src/components/ui/separator.jsx",
      "/app/frontend/src/components/ui/scroll-area.jsx",
      "/app/frontend/src/components/ui/skeleton.jsx",
      "/app/frontend/src/components/ui/dialog.jsx",
      "/app/frontend/src/components/ui/sheet.jsx",
      "/app/frontend/src/components/ui/alert.jsx",
      "/app/frontend/src/components/ui/alert-dialog.jsx",
      "/app/frontend/src/components/ui/sonner.jsx"
    ],
    "recommended_new_components_js": [
      {
        "name": "FileDropzone",
        "path": "/app/frontend/src/components/FileDropzone.js",
        "notes": "Use react-dropzone or native drag events; show file chip + remove; validate PDF/DOCX; include data-testid on zone and remove button."
      },
      {
        "name": "ScoreRing",
        "path": "/app/frontend/src/components/ScoreRing.js",
        "notes": "Small SVG ring for score out of 10; used in summary + section headers."
      },
      {
        "name": "ReportSection",
        "path": "/app/frontend/src/components/ReportSection.js",
        "notes": "Renders issues/recommendations/examples/resources with consistent subheadings and copy buttons."
      },
      {
        "name": "ReviewHistoryPanel",
        "path": "/app/frontend/src/components/ReviewHistoryPanel.js",
        "notes": "Desktop sidebar + mobile Sheet; list items clickable; search input; delete confirm dialog."
      }
    ],
    "icons": {
      "library": "lucide-react",
      "suggested": [
        "Upload",
        "FileText",
        "Sparkles",
        "CheckCircle2",
        "AlertTriangle",
        "Copy",
        "Trash2",
        "History",
        "Search"
      ]
    }
  },
  "key_ui_patterns": {
    "submission": {
      "tabs": [
        {
          "id": "upload",
          "title": "Upload PDF/DOCX",
          "content": "Dropzone + file preview + privacy note"
        },
        {
          "id": "paste",
          "title": "Paste CV text",
          "content": "Textarea with character count + formatting tips"
        }
      ],
      "optional_context": {
        "pattern": "Collapsible titled 'Tailor to a role (optional)'",
        "fields": [
          "Target job title",
          "Industry",
          "Job description (textarea)"
        ]
      },
      "validation": [
        "Disable submit until file or text present",
        "Show inline errors in Alert component",
        "File size limit hint (e.g., 10MB)"
      ]
    },
    "results": {
      "summary_row": {
        "cards": [
          "Overall score",
          "Top strengths",
          "Top improvements"
        ],
        "layout": "grid grid-cols-1 md:grid-cols-3 gap-4"
      },
      "section_accordion": {
        "sections": [
          "Personal Information and Contact Details",
          "Format and Structure",
          "Professional Experience",
          "Education",
          "Skills and Competencies",
          "Language Proficiency",
          "Hobbies and Interests",
          "Cultural Fit and Adaptability",
          "General Recommendations"
        ],
        "header": "Left: section title; Right: score badge + small ring",
        "inside": "Three blocks: Strengths, Issues, Actionable recommendations; plus STAR rewrite examples when relevant"
      },
      "resources_block": {
        "pattern": "Card with link list + short descriptions",
        "links": [
          {
            "label": "InfoFinland — Job application and CV",
            "url": "https://infofinland.fi/work-and-enterprise/find-a-job-in-finland/job-application-and-cv"
          },
          {
            "label": "VisualCV — Finland resume guide",
            "url": "https://www.visualcv.com/international/finland-resume/"
          }
        ]
      }
    },
    "history": {
      "desktop": "Sticky sidebar with ScrollArea",
      "mobile": "History button opens Sheet from bottom/right",
      "empty_state": "Show Skeleton list on load; show friendly empty message with CTA to run first review"
    }
  },
  "motion_and_microinteractions": {
    "principles": [
      "Motion should communicate state: uploading, analyzing, completed",
      "Prefer subtle translate/opacity; avoid large bouncy animations",
      "Respect prefers-reduced-motion"
    ],
    "recommended_library": {
      "name": "framer-motion",
      "install": "npm i framer-motion",
      "usage": [
        "Animate report entrance: initial {opacity:0,y:8} → animate {opacity:1,y:0}",
        "Accordion content fade-in",
        "Button press scale: whileTap {scale:0.98}"
      ]
    },
    "hover_states": {
      "buttons": "hover:brightness-[0.98] active:translate-y-[1px] transition-colors",
      "cards": "hover:shadow-[var(--shadow-lift)] transition-shadow",
      "dropzone": "on drag active: ring-2 ring-primary/40 bg-accent/40"
    },
    "loading": {
      "pattern": "Progress + stepper + skeleton blocks for each report section",
      "progress_component": "shadcn Progress"
    }
  },
  "accessibility": {
    "requirements": [
      "WCAG AA contrast for text and controls",
      "Visible focus ring using --focus token",
      "Keyboard navigable tabs/accordion/dialog/sheet (shadcn defaults)",
      "Use aria-describedby for helper text and errors",
      "Provide file input label and accepted types"
    ],
    "content_tone": [
      "Avoid shaming language; use coaching phrasing",
      "Explain Finnish norms neutrally (e.g., photo optional, references with consent)"
    ]
  },
  "data_testid_conventions": {
    "rule": "All interactive and key informational elements MUST include data-testid.",
    "examples": [
      "data-testid=\"hero-start-review-button\"",
      "data-testid=\"cv-upload-dropzone\"",
      "data-testid=\"cv-upload-file-input\"",
      "data-testid=\"cv-text-paste-textarea\"",
      "data-testid=\"context-job-title-input\"",
      "data-testid=\"context-industry-input\"",
      "data-testid=\"context-job-description-textarea\"",
      "data-testid=\"run-review-submit-button\"",
      "data-testid=\"analysis-progress-bar\"",
      "data-testid=\"overall-score\"",
      "data-testid=\"report-section-accordion\"",
      "data-testid=\"report-copy-rewrite-button\"",
      "data-testid=\"history-open-sheet-button\"",
      "data-testid=\"history-item-button\"",
      "data-testid=\"history-delete-button\""
    ]
  },
  "image_urls": {
    "hero": [
      {
        "url": "https://images.unsplash.com/photo-1544717297-fa95b6ee9643?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1MTN8MHwxfHNlYXJjaHwxfHxub3JkaWMlMjBvZmZpY2UlMjBkZXNrJTIwbWluaW1hbCUyMHJlc3VtZSUyMGRvY3VtZW50c3xlbnwwfHx8dGVhbHwxNzc3NDc1NDM0fDA&ixlib=rb-4.1.0&q=85",
        "description": "Nordic desk scene for hero side image (use as subtle, desaturated cover in a card)."
      }
    ],
    "empty_states_or_side_panel": [
      {
        "url": "https://images.pexels.com/photos/3205566/pexels-photo-3205566.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "description": "Optional small thumbnail for history empty state illustration (use sparingly; keep it small)."
      }
    ]
  },
  "implementation_notes_for_main_agent": {
    "css_updates": [
      "Replace default CRA App.css usage; avoid .App {text-align:center}.",
      "Update index.css :root tokens to the teal/sand system above.",
      "Add font-family utilities via Tailwind config or apply in body: font-family: var(--font-body)."
    ],
    "recommended_global_classes": {
      "body": "font-[Figtree]",
      "headings": "font-[Space_Grotesk]",
      "page_bg": "bg-background text-foreground",
      "card": "bg-card text-card-foreground shadow-[var(--shadow-soft)]"
    },
    "file_upload": {
      "accepted": ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
      "ui": "Show file chip with remove; show parsing note; show privacy note under dropzone",
      "errors": "Use Alert component; toast for transient errors via sonner"
    },
    "report_rendering": {
      "pattern": "Use Accordion for sections; each section includes ScoreRing + Badge; include Copy buttons for examples",
      "copy": "Use navigator.clipboard.writeText; toast success"
    },
    "history": {
      "pattern": "Desktop sticky sidebar; mobile Sheet",
      "item": "Clickable row with title + date; include reopen button"
    },
    "performance": [
      "Lazy-render accordion content (render on open) if report is large",
      "Use ScrollArea for long report",
      "Avoid heavy images; keep hero image small and compressed"
    ]
  },
  "general_ui_ux_design_guidelines_appendix": "<General UI UX Design Guidelines>  \n    - You must **not** apply universal transition. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms\n    - You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text\n   - NEVER: use AI assistant Emoji characters like`🤖🧠💭💡🔮🎯📚🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎰💰💵💳🏦💎🪙💸🤑📊📈📉💹🔢🏆🥇 etc for icons. Always use **FontAwesome cdn** or **lucid-react** library already installed in the package.json\n\n **GRADIENT RESTRICTION RULE**\nNEVER use dark/saturated gradient combos (e.g., purple/pink) on any UI element.  Prohibited gradients: blue-500 to purple 600, purple 500 to pink-500, green-500 to blue-500, red to pink etc\nNEVER use dark gradients for logo, testimonial, footer etc\nNEVER let gradients cover more than 20% of the viewport.\nNEVER apply gradients to text-heavy content or reading areas.\nNEVER use gradients on small UI elements (<100px width).\nNEVER stack multiple gradient layers in the same viewport.\n\n**ENFORCEMENT RULE:**\n    • Id gradient area exceeds 20% of viewport OR affects readability, **THEN** use solid colors\n\n**How and where to use:**\n   • Section backgrounds (not content backgrounds)\n   • Hero section header content. Eg: dark to light to dark color\n   • Decorative overlays and accent elements only\n   • Hero section with 2-3 mild color\n   • Gradients creation can be done for any angle say horizontal, vertical or diagonal\n\n- For AI chat, voice application, **do not use purple color. Use color like light green, ocean blue, peach orange etc**\n\n</Font Guidelines>\n\n- Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations. Static = dead. \n   \n- Use 2-3x more spacing than feels comfortable. Cramped designs look cheap.\n\n- Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations: separates good from extraordinary.\n   \n- Before generating UI, infer the visual style from the problem statement (palette, contrast, mood, motion) and immediately instantiate it by setting global design tokens (primary, secondary/accent, background, foreground, ring, state colors), rather than relying on any library defaults. Don't make the background dark as a default step, always understand problem first and define colors accordingly\n    Eg: - if it implies playful/energetic, choose a colorful scheme\n           - if it implies monochrome/minimal, choose a black–white/neutral scheme\n\n**Component Reuse:**\n\t- Prioritize using pre-existing components from src/components/ui when applicable\n\t- Create new components that match the style and conventions of existing components when needed\n\t- Examine existing components to understand the project's component patterns before creating new ones\n\n**IMPORTANT**: Do not use HTML based component like dropdown, calendar, toast etc. You **MUST** always use `/app/frontend/src/components/ui/ ` only as a primary components as these are modern and stylish component\n\n**Best Practices:**\n\t- Use Shadcn/UI as the primary component library for consistency and accessibility\n\t- Import path: ./components/[component-name]\n\n**Export Conventions:**\n\t- Components MUST use named exports (export const ComponentName = ...)\n\t- Pages MUST use default exports (export default function PageName() {...})\n\n**Toasts:**\n  - Use `sonner` for toasts\"\n  - Sonner component are located in `/app/src/components/ui/sonner.tsx`\n\nUse 2–4 color gradients, subtle textures/noise overlays, or CSS-based noise to avoid flat visuals.\n</General UI UX Design Guidelines>"
}
