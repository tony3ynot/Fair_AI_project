# Claude Code Guidelines - Fair AI Project

This document contains guidelines for efficient collaboration with Claude on the Fair AI Project.

## 🚫 Never Do These

### Database
- **NEVER USE SQLITE. USE MYSQL.**
- Never use mock data or hardcoded data in the code
- Always fetch data from the actual database and strictly follow the database schema

### Type Safety
- Never use `any` type or generic types like `Dict[str, Any]`
- Always use specific, concrete type annotations

### Security
- Passwords must be hashed with bcrypt, Argon2, or scrypt (never MD5, SHA1, or plain SHA256)
- Prevent SQL injection: always use parameterized queries
- Never hardcode sensitive information in code
- Never commit `.env` files to Git

## ✅ Always Follow These

### Development Environment
- **Timezone**: Always use UTC+9 (Korea Standard Time)
- **Docker**: Backend and database run on Docker
- **Port Management**: Kill and restart processes if ports are in use (never change port numbers)

### Code Quality
- Delete temporary debugging files after use
- Remove unnecessary files after careful consideration
- Write clean, reusable, and maintainable code
- Add appropriate comments when needed

### UI/UX
- **Design**: Maintain consistent light mode style (disable dark mode)
- Avoid overly fancy frontend designs
- Don't add features not specified by the database structure

## 🛠 Technology Stack Guidelines

### Backend (FastAPI)
```python
# Good Example
from typing import List, Optional
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool

# Bad Example
def get_user(id: Any) -> Dict[str, Any]:  # ❌ Using Any type
    return {"id": id, "email": "test@test.com"}
```

### Frontend (React + TypeScript)
- **Styling**: Use Tailwind CSS (no CSS-in-JS or styled-components)
- **Environment Variables**: Use `VITE_` prefix (e.g., `VITE_API_BASE_URL`)
- **Routing**: Use React Router
- **State Management**: Use React Query
- **Business Logic**: Separate into custom hooks

```typescript
// Good Example
// useUser.ts - Business logic
export const useUser = (userId: number) => {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });
};

// UserProfile.tsx - UI only
const UserProfile = ({ userId }: { userId: number }) => {
  const { data: user, isLoading } = useUser(userId);
  // UI rendering only
};
```

## 📋 Project Workflow

1. **Break complex tasks into smaller units**
2. **Verify each step works before proceeding**
3. **Ensure type safety**
4. **Validate security**
5. **Clean up unnecessary files**

## 🔒 Security Checklist

### API Security
- [ ] Implement rate limiting (e.g., 100 requests per minute)
- [ ] Configure CORS properly (never use `*` in production)
- [ ] Validate and sanitize all inputs
- [ ] Validate JWT tokens
- [ ] Use HTTPS

### Data Protection
- [ ] Encrypt sensitive data (AES-256)
- [ ] Prevent sensitive information in logs
- [ ] Restrict file uploads (type, size)

### Error Handling
- [ ] Never expose stack traces
- [ ] Use generic error messages for users
- [ ] Detailed server-side logging

## 💡 Development Tips

### Python Troubleshooting
- If Python doesn't work well, check `backend/venv/bin/python`

### Docker Commands
```bash
# Access MySQL
docker exec -it fair_ai_mysql mysql -u root -p

# Check backend logs
docker logs fair_ai_backend -f

# Restart container
docker-compose restart backend
```

### Git Commit Messages
- Write clear and specific messages
- Feature addition: `feat: `
- Bug fix: `fix: `
- Refactoring: `refactor: `
- Documentation update: `docs: `

## 🚀 Quick Commands

```bash
# Start development environment
docker-compose up -d

# Frontend development
cd frontend-mvp && npm run dev

# Backend development (outside Docker)
cd backend && uvicorn app.main:app --reload

# Type check
cd backend && mypy .

# Run lint
cd frontend-mvp && npm run lint
```

## 📦 Package Management

- **Never install packages directly** - always ask the user first
- Keep dependencies minimal and well-justified
- Regular security audits with `npm audit` and `pip-audit`

## 🎯 Key Principles

1. **When in doubt, choose the more secure option**
2. **Always assume user input is malicious**
3. **Defense in depth - use multiple layers of security**
4. **Test security measures before deploying to production**

---

**Remember**: Security and type safety are not optional - they are fundamental requirements!