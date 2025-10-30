"""
CodeGalaxy - UI Components
Reusable UI components with glassmorphism design
"""

import streamlit as st

# ============================================================
# BUTTON COMPONENTS
# ============================================================

def gradient_button(text, key, icon=None, onclick=None):
    """
    Returns HTML/CSS for gradient button
    Args:
        text: Button text
        key: Unique button key
        icon: Optional icon (emoji or HTML)
        onclick: Optional onclick handler
    Returns: HTML string
    """
    icon_html = f"{icon} " if icon else ""

    return f"""
    <style>
        .gradient-btn-{key} {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 16px;
            display: inline-block;
            text-align: center;
            width: 100%;
        }}
        .gradient-btn-{key}:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }}
    </style>
    <button class="gradient-btn-{key}" onclick="{onclick if onclick else ''}">{icon_html}{text}</button>
    """

# ============================================================
# CARD COMPONENTS
# ============================================================

def glass_card(content, width="100%", padding="20px"):
    """
    Returns HTML for glassmorphism card
    Args:
        content: Card content (HTML)
        width: Card width
        padding: Card padding
    Returns: HTML string
    """
    return f"""
    <div style='
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        padding: {padding};
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        width: {width};
    '>
        {content}
    </div>
    """

def stats_card(value, label, icon="📊"):
    """
    Returns HTML for stats card
    Args:
        value: Stat value (number or text)
        label: Stat label
        icon: Icon emoji or HTML
    Returns: HTML string
    """
    return f"""
    <div style='
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        transition: all 0.3s ease;
    '>
        <div style='font-size: 48px; margin-bottom: 10px;'>{icon}</div>
        <div style='font-size: 36px; font-weight: bold; color: #667eea; margin: 10px 0;'>{value}</div>
        <div style='color: #999; font-size: 14px;'>{label}</div>
    </div>
    """

def model_card(model_name, description, icon="🤖", selected=False):
    """
    Returns HTML for model selection card
    Args:
        model_name: Name of the model
        description: Model description
        icon: Model icon
        selected: Whether card is selected
    Returns: HTML string
    """
    border_color = "#667eea" if selected else "rgba(255, 255, 255, 0.3)"
    bg_opacity = "0.2" if selected else "0.1"

    return f"""
    <div style='
        background: rgba(255, 255, 255, {bg_opacity});
        backdrop-filter: blur(10px);
        border: 2px solid {border_color};
        border-radius: 16px;
        padding: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
    '>
        <div style='font-size: 48px; margin-bottom: 10px;'>{icon}</div>
        <div style='font-size: 20px; font-weight: bold; color: white; margin: 10px 0;'>{model_name}</div>
        <div style='color: #ccc; font-size: 14px;'>{description}</div>
    </div>
    """

# ============================================================
# BADGE COMPONENTS
# ============================================================

def badge(text, color="default"):
    """
    Returns HTML for badge/pill component
    Args:
        text: Badge text
        color: "default", "success", "danger", "warning", "info"
    Returns: HTML string
    """
    colors = {
        "default": "#999",
        "success": "#10b981",
        "danger": "#ef4444",
        "warning": "#f59e0b",
        "info": "#3b82f6"
    }

    bg_color = colors.get(color, colors["default"])

    return f"""
    <span style='
        background: {bg_color};
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin: 2px;
    '>{text}</span>
    """

def star_rating(rating, size="medium"):
    """
    Returns HTML for star rating display
    Args:
        rating: Rating value (1-5)
        size: "small", "medium", "large"
    Returns: HTML string
    """
    sizes = {
        "small": "16px",
        "medium": "24px",
        "large": "32px"
    }

    font_size = sizes.get(size, sizes["medium"])

    stars = []
    for i in range(5):
        if i < rating:
            stars.append(f"<span style='color: #fbbf24; font-size: {font_size};'>★</span>")
        else:
            stars.append(f"<span style='color: #444; font-size: {font_size};'>★</span>")

    return "".join(stars)

# ============================================================
# CODE DISPLAY
# ============================================================

def code_block(code, language="python", show_line_numbers=True):
    """
    Returns HTML for syntax-highlighted code block
    Args:
        code: Code content
        language: Programming language
        show_line_numbers: Whether to show line numbers
    Returns: HTML string
    """
    lines = code.split('\n')
    line_numbers = ""
    code_lines = ""

    if show_line_numbers:
        for i, line in enumerate(lines, 1):
            line_numbers += f"<div style='color: #666; text-align: right; padding-right: 10px;'>{i}</div>"
            code_lines += f"<div>{line if line else ' '}</div>"

        return f"""
        <div style='
            background: #1e1e1e;
            border-radius: 12px;
            overflow: hidden;
            font-family: "Courier New", monospace;
            font-size: 14px;
        '>
            <div style='
                background: #2d2d2d;
                padding: 10px 20px;
                color: #ccc;
                font-weight: 600;
            '>{language}</div>
            <div style='display: flex; padding: 20px 0;'>
                <div style='flex-shrink: 0;'>{line_numbers}</div>
                <div style='flex-grow: 1; padding-left: 20px; color: #f8f8f2;'>{code_lines}</div>
            </div>
        </div>
        """
    else:
        return f"""
        <div style='
            background: #1e1e1e;
            border-radius: 12px;
            overflow: hidden;
            font-family: "Courier New", monospace;
            font-size: 14px;
        '>
            <div style='
                background: #2d2d2d;
                padding: 10px 20px;
                color: #ccc;
                font-weight: 600;
            '>{language}</div>
            <div style='padding: 20px; color: #f8f8f2;'>
                <pre style='margin: 0;'>{code}</pre>
            </div>
        </div>
        """

# ============================================================
# LOADING/ANIMATION COMPONENTS
# ============================================================

def loading_spinner(message="Loading..."):
    """
    Returns HTML/CSS for animated loading spinner
    Args:
        message: Loading message
    Returns: HTML string
    """
    return f"""
    <style>
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        .spinner {{
            border: 4px solid rgba(255, 255, 255, 0.1);
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }}
    </style>
    <div style='text-align: center; padding: 40px;'>
        <div class='spinner'></div>
        <div style='color: #999; margin-top: 20px;'>{message}</div>
    </div>
    """

def progress_bar(percentage, color="#667eea"):
    """
    Returns HTML for progress bar
    Args:
        percentage: Progress percentage (0-100)
        color: Bar color
    Returns: HTML string
    """
    return f"""
    <div style='
        width: 100%;
        height: 24px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        overflow: hidden;
    '>
        <div style='
            width: {percentage}%;
            height: 100%;
            background: linear-gradient(90deg, {color} 0%, #764ba2 100%);
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 12px;
        '>{percentage}%</div>
    </div>
    """

# ============================================================
# NOTIFICATION COMPONENTS
# ============================================================

def success_message(message):
    """
    Returns HTML for success notification
    Args:
        message: Success message
    Returns: HTML string
    """
    return f"""
    <div style='
        background: rgba(16, 185, 129, 0.2);
        border-left: 4px solid #10b981;
        padding: 16px;
        border-radius: 8px;
        color: #10b981;
        margin: 10px 0;
    '>
        ✓ {message}
    </div>
    """

def error_message(message):
    """
    Returns HTML for error notification
    Args:
        message: Error message
    Returns: HTML string
    """
    return f"""
    <div style='
        background: rgba(239, 68, 68, 0.2);
        border-left: 4px solid #ef4444;
        padding: 16px;
        border-radius: 8px;
        color: #ef4444;
        margin: 10px 0;
    '>
        ✕ {message}
    </div>
    """

def info_message(message):
    """
    Returns HTML for info notification
    Args:
        message: Info message
    Returns: HTML string
    """
    return f"""
    <div style='
        background: rgba(59, 130, 246, 0.2);
        border-left: 4px solid #3b82f6;
        padding: 16px;
        border-radius: 8px;
        color: #3b82f6;
        margin: 10px 0;
    '>
        ℹ {message}
    </div>
    """

# ============================================================
# HEADER COMPONENTS
# ============================================================

def page_header(title, subtitle=None, icon=None):
    """
    Returns HTML for page header
    Args:
        title: Page title
        subtitle: Optional subtitle
        icon: Optional icon
    Returns: HTML string
    """
    icon_html = f"<span style='margin-right: 10px;'>{icon}</span>" if icon else ""
    subtitle_html = f"<p style='color: #999; font-size: 16px; margin-top: 10px;'>{subtitle}</p>" if subtitle else ""

    return f"""
    <div style='margin-bottom: 30px;'>
        <h1 style='
            font-size: 36px;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        '>
            {icon_html}{title}
        </h1>
        {subtitle_html}
    </div>
    """

# ============================================================
# TABLE COMPONENTS
# ============================================================

def data_table(headers, rows):
    """
    Returns HTML for data table
    Args:
        headers: List of header strings
        rows: List of row lists
    Returns: HTML string
    """
    header_html = "".join([f"<th style='padding: 12px; text-align: left; border-bottom: 2px solid #667eea;'>{h}</th>" for h in headers])

    rows_html = ""
    for row in rows:
        cells = "".join([f"<td style='padding: 12px; border-bottom: 1px solid rgba(255,255,255,0.1);'>{cell}</td>" for cell in row])
        rows_html += f"<tr>{cells}</tr>"

    return f"""
    <div style='overflow-x: auto;'>
        <table style='
            width: 100%;
            border-collapse: collapse;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            overflow: hidden;
        '>
            <thead style='background: rgba(102, 126, 234, 0.2);'>
                <tr>{header_html}</tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """

# ============================================================
# MODAL/DIALOG COMPONENTS
# ============================================================

def confirm_dialog(title, message, confirm_text="Confirm", cancel_text="Cancel"):
    """
    Returns HTML for confirmation dialog
    Args:
        title: Dialog title
        message: Dialog message
        confirm_text: Confirm button text
        cancel_text: Cancel button text
    Returns: HTML string
    """
    return f"""
    <div style='
        background: rgba(0, 0, 0, 0.5);
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    '>
        <div style='
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 16px;
            padding: 30px;
            max-width: 400px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        '>
            <h2 style='margin-top: 0; color: white;'>{title}</h2>
            <p style='color: #ccc;'>{message}</p>
            <div style='display: flex; gap: 10px; margin-top: 20px;'>
                <button style='
                    flex: 1;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 12px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: 600;
                '>{confirm_text}</button>
                <button style='
                    flex: 1;
                    background: rgba(255, 255, 255, 0.1);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    padding: 12px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: 600;
                '>{cancel_text}</button>
            </div>
        </div>
    </div>
    """

# ============================================================
# EMPTY STATE COMPONENTS
# ============================================================

def empty_state(icon="📭", title="No Data", message="There's nothing here yet", action_text=None):
    """
    Returns HTML for empty state
    Args:
        icon: Icon emoji
        title: Empty state title
        message: Empty state message
        action_text: Optional action button text
    Returns: HTML string
    """
    action_html = ""
    if action_text:
        action_html = f"""
        <button style='
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            margin-top: 20px;
        '>{action_text}</button>
        """

    return f"""
    <div style='
        text-align: center;
        padding: 60px 20px;
        color: #999;
    '>
        <div style='font-size: 64px; margin-bottom: 20px;'>{icon}</div>
        <h3 style='color: #ccc; margin: 10px 0;'>{title}</h3>
        <p>{message}</p>
        {action_html}
    </div>
    """
