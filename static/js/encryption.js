/**
 * AFL Tipping App - Encryption/Decryption Functions
 * Uses CryptoJS for client-side encryption with AES
 */

/**
 * Encrypt tip data with password
 * @param {Object} tipData - The tip data to encrypt
 * @param {string} password - The password for encryption
 * @returns {string} Encrypted string
 */
function encryptTipData(tipData, password) {
    try {
        // Convert tip data to JSON string
        const jsonString = JSON.stringify(tipData);
        
        // Encrypt using AES with the password
        const encrypted = CryptoJS.AES.encrypt(jsonString, password).toString();
        
        return encrypted;
    } catch (error) {
        console.error('Encryption error:', error);
        throw new Error('Failed to encrypt tip data');
    }
}

/**
 * Decrypt tip data with password
 * @param {string} encryptedString - The encrypted string
 * @param {string} password - The password for decryption
 * @returns {Object|null} Decrypted tip data or null if failed
 */
function decryptTipData(encryptedString, password) {
    try {
        // Decrypt using AES with the password
        const decryptedBytes = CryptoJS.AES.decrypt(encryptedString, password);
        const decryptedString = decryptedBytes.toString(CryptoJS.enc.Utf8);
        
        if (!decryptedString) {
            throw new Error('Decryption failed - invalid password or corrupted data');
        }
        
        // Parse JSON string back to object
        const tipData = JSON.parse(decryptedString);
        
        return tipData;
    } catch (error) {
        console.error('Decryption error:', error);
        return null;
    }
}

/**
 * Validate encrypted string format
 * @param {string} encryptedString - The encrypted string to validate
 * @returns {boolean} True if valid format
 */
function validateEncryptedString(encryptedString) {
    if (!encryptedString || typeof encryptedString !== 'string') {
        return false;
    }
    
    // Basic validation - encrypted strings should be base64-like
    const base64Regex = /^[A-Za-z0-9+/=]+$/;
    return base64Regex.test(encryptedString) && encryptedString.length > 20;
}

/**
 * Generate a random password suggestion
 * @param {number} length - Length of password (default 8)
 * @returns {string} Random password
 */
function generateRandomPassword(length = 8) {
    const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let password = '';
    
    for (let i = 0; i < length; i++) {
        password += charset.charAt(Math.floor(Math.random() * charset.length));
    }
    
    return password;
}

/**
 * Copy text to clipboard with fallback
 * @param {string} text - Text to copy
 * @returns {boolean} Success status
 */
function copyToClipboardAdvanced(text) {
    try {
        // Modern browser method
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text);
            return true;
        }
        
        // Fallback method
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        const success = document.execCommand('copy');
        textArea.remove();
        
        return success;
    } catch (error) {
        console.error('Copy to clipboard failed:', error);
        return false;
    }
}

/**
 * Format tip data for display
 * @param {Object} tipData - The tip data object
 * @returns {string} Formatted string for display
 */
function formatTipDataForDisplay(tipData) {
    let formatted = `Tipper: ${tipData.user_name}\n`;
    formatted += `Round: ${tipData.round || 'Round 24'}\n`;
    formatted += `Date: ${tipData.created_at || new Date().toISOString().split('T')[0]}\n\n`;
    
    formatted += 'Tips:\n';
    Object.entries(tipData.tips).forEach(([gameId, team]) => {
        formatted += `Game ${gameId}: ${team}\n`;
    });
    
    if (tipData.margin) {
        formatted += `\nMargin Prediction: ${tipData.margin} points\n`;
    }
    
    return formatted;
}

// Export functions for use in other scripts (if using modules)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        encryptTipData,
        decryptTipData,
        validateEncryptedString,
        generateRandomPassword,
        copyToClipboardAdvanced,
        formatTipDataForDisplay
    };
}
