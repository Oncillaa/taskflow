// utils/notifications.js

const NOTIFICATION_TYPES = {
    SUCCESS: 'success',
    ERROR: 'error',
    WARNING: 'warning',
    INFO: 'info'
};

const STYLES = {
    success: { bg: '#4CAF50', icon: '✅' },
    error: { bg: '#f44336', icon: '❌' },
    warning: { bg: '#ff9800', icon: '⚠️' },
    info: { bg: '#2196F3', icon: 'ℹ️' }
};

export function showNotification(message, type = NOTIFICATION_TYPES.INFO) {
    const style = STYLES[type] || STYLES.info;

    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: ${style.bg};
        color: white;
        padding: 16px 24px;
        border-radius: 10px;
        font-size: 16px;
        font-family: Arial, sans-serif;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        z-index: 999999;
        display: flex;
        align-items: center;
        gap: 12px;
        animation: slideIn 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        max-width: 450px;
    `;

    notification.innerHTML = `
        <span style="font-size: 28px;">${style.icon}</span>
        <span>${message}</span>
    `;

    document.body.appendChild(notification);

    // Добавляем стили анимации, если ещё нет
    if (!document.getElementById('notification-styles')) {
        const styleTag = document.createElement('style');
        styleTag.id = 'notification-styles';
        styleTag.textContent = `
            @keyframes slideIn {
                0% { transform: translateX(120%) scale(0.8); opacity: 0; }
                100% { transform: translateX(0) scale(1); opacity: 1; }
            }
            @keyframes fadeOut {
                0% { opacity: 1; transform: translateX(0); }
                100% { opacity: 0; transform: translateX(50px); }
            }
        `;
        document.head.appendChild(styleTag);
    }

    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease forwards';
        setTimeout(() => notification.remove(), 300);
    }, 3500);
}

export const notify = {
    success: (msg) => showNotification(msg, NOTIFICATION_TYPES.SUCCESS),
    error: (msg) => showNotification(msg, NOTIFICATION_TYPES.ERROR),
    warning: (msg) => showNotification(msg, NOTIFICATION_TYPES.WARNING),
    info: (msg) => showNotification(msg, NOTIFICATION_TYPES.INFO)
};