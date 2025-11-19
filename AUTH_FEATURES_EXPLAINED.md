# Why Refresh Tokens and OTP?

## 🔐 OTP (One-Time Password) - Why You Need It

### Use Cases:

1. **Email/Phone Verification**
   - Verify user's email or phone number is real
   - Prevent fake accounts
   - Required before allowing access to sensitive features

2. **Password Reset**
   - User forgets password → Send OTP to email/phone
   - Verify identity before allowing password change
   - More secure than just email links

3. **Two-Factor Authentication (2FA)**
   - Extra security layer
   - Even if password is stolen, attacker needs OTP
   - Common in banking, payment apps

4. **Login Verification**
   - Optional: Require OTP for login from new device
   - Prevents unauthorized access

### Example Flow:
```
User registers → OTP sent to email → User enters OTP → Account verified ✅
User forgets password → OTP sent → User enters OTP → Can reset password ✅
```

### In Your Code:
- `POST /api/auth/send-otp` - Generate and send OTP
- `POST /api/auth/verify-otp` - Verify OTP and mark user as verified
- OTP expires in 5 minutes (security)
- Rate limited (max 3 OTPs per 5 minutes)

---

## 🔄 Refresh Tokens - Why You Need It

### The Problem:
- JWT tokens expire (for security - e.g., 7 days)
- When token expires, user must login again
- Bad user experience for mobile apps, long sessions

### The Solution: Refresh Tokens

1. **Access Token (JWT)**
   - Short-lived (e.g., 15 minutes - 1 hour)
   - Used for API requests
   - If stolen, expires quickly

2. **Refresh Token**
   - Long-lived (e.g., 30 days)
   - Used ONLY to get new access tokens
   - Stored securely (httpOnly cookie or secure storage)

### Flow:
```
Login → Get access_token (1 hour) + refresh_token (30 days)
↓
Access token expires after 1 hour
↓
Use refresh_token → Get new access_token
↓
No need to login again! ✅
```

### Benefits:

1. **Better Security**
   - Access tokens expire quickly (less damage if stolen)
   - Refresh tokens can be revoked
   - Can detect token theft

2. **Better UX**
   - Users stay logged in for weeks
   - No frequent re-logins
   - Mobile apps work smoothly

3. **Session Management**
   - Can revoke refresh tokens (logout all devices)
   - Can track active sessions
   - Better control

### In Your Code:
- `POST /api/auth/refresh` - Exchange refresh token for new access token
- Currently supports Supabase Auth mode
- Can be extended for custom JWT mode

---

## 🎯 When to Use Each

### Use OTP When:
- ✅ Verifying email/phone during registration
- ✅ Resetting forgotten password
- ✅ Enabling 2FA for extra security
- ✅ Login from new device (optional)
- ✅ Sensitive operations (payment, account changes)

### Use Refresh Tokens When:
- ✅ Building mobile apps (iOS/Android)
- ✅ Long user sessions needed
- ✅ Better security (short-lived access tokens)
- ✅ Need to revoke sessions remotely
- ✅ Multiple devices support

---

## 📊 Your Current Implementation

### OTP Features:
```python
# Send OTP
POST /api/auth/send-otp
{
  "target": "user@example.com",
  "type": "register" | "login" | "reset"
}

# Verify OTP
POST /api/auth/verify-otp
{
  "target": "user@example.com",
  "code": "123456",
  "type": "register"
}
```

### Refresh Token Features:
```python
# Refresh token (Supabase Auth mode)
POST /api/auth/refresh
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

## 💡 Real-World Examples

### OTP Examples:
- **Gmail**: Sends OTP when logging in from new device
- **Banking Apps**: OTP for every transaction
- **WhatsApp**: OTP to verify phone number
- **GitHub**: OTP for 2FA

### Refresh Token Examples:
- **Mobile Apps**: Stay logged in for weeks
- **Web Apps**: "Remember me" functionality
- **APIs**: Long-running background jobs
- **Social Media**: Stay logged in across devices

---

## 🔧 Optional vs Required

### OTP:
- **Optional** - You can disable if not needed
- Remove OTP verification step if you don't need it
- Keep it for better security

### Refresh Tokens:
- **Optional** - Works without it (just shorter sessions)
- Access tokens expire, user logs in again
- Add it for better UX and security

---

## Summary

| Feature | Purpose | When to Use |
|---------|---------|-------------|
| **OTP** | Verify identity | Registration, password reset, 2FA |
| **Refresh Tokens** | Maintain sessions | Mobile apps, long sessions, better security |

Both are **optional** but **recommended** for production apps! 🚀

