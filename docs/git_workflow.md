# Git Workflow

## Overview
This document outlines the Git workflow and branching strategy for the Ontario Driving School Manager application.

## Branch Strategy

### Main Branches
- `main`: Production-ready code
- `develop`: Integration branch for features
- `release/*`: Release preparation branches
- `hotfix/*`: Production fixes
- `feature/*`: New features
- `bugfix/*`: Bug fixes

### Branch Naming
- Features: `feature/description-of-feature`
- Bugs: `bugfix/description-of-bug`
- Releases: `release/v1.0.0`
- Hotfixes: `hotfix/description-of-fix`

## Workflow

### Feature Development
1. Create feature branch from `develop`
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/new-feature
   ```

2. Develop and commit changes
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

3. Keep branch up to date
   ```bash
   git checkout develop
   git pull
   git checkout feature/new-feature
   git rebase develop
   ```

4. Create pull request to `develop`

### Bug Fixes
1. Create bugfix branch from `develop`
   ```bash
   git checkout develop
   git pull
   git checkout -b bugfix/description
   ```

2. Fix and commit changes
   ```bash
   git add .
   git commit -m "fix: resolve bug"
   ```

3. Create pull request to `develop`

### Releases
1. Create release branch from `develop`
   ```bash
   git checkout develop
   git pull
   git checkout -b release/v1.0.0
   ```

2. Version bump and final fixes
   ```bash
   git commit -m "chore: bump version to 1.0.0"
   ```

3. Merge to `main` and `develop`
   ```bash
   git checkout main
   git merge release/v1.0.0
   git tag -a v1.0.0 -m "Version 1.0.0"
   git checkout develop
   git merge release/v1.0.0
   ```

### Hotfixes
1. Create hotfix branch from `main`
   ```bash
   git checkout main
   git pull
   git checkout -b hotfix/description
   ```

2. Fix and commit changes
   ```bash
   git add .
   git commit -m "fix: resolve critical issue"
   ```

3. Merge to `main` and `develop`
   ```bash
   git checkout main
   git merge hotfix/description
   git tag -a v1.0.1 -m "Version 1.0.1"
   git checkout develop
   git merge hotfix/description
   ```

## Commit Messages

### Format
```
type(scope): subject

body

footer
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Testing
- `chore`: Maintenance

### Examples
```
feat(auth): add OAuth2 authentication

- Implement Google OAuth2
- Add token management
- Update documentation

Closes #123
```

```
fix(api): resolve data validation error

- Add input validation
- Update error handling
- Add test cases

Fixes #456
```

## Pull Requests

### Process
1. Create pull request
2. Add description
3. Link related issues
4. Request reviewers
5. Address feedback
6. Merge after approval

### Requirements
- Passing tests
- Code review approval
- No merge conflicts
- Updated documentation
- Follows coding standards

## Code Review

### Guidelines
- Review for functionality
- Check code quality
- Verify test coverage
- Ensure documentation
- Look for security issues

### Process
1. Review code changes
2. Add comments
3. Request changes if needed
4. Approve when satisfied

## Continuous Integration

### Checks
- Unit tests
- Integration tests
- Linting
- Type checking
- Security scanning

### Process
1. Push changes
2. Wait for CI checks
3. Address any failures
4. Proceed with merge

## Deployment

### Process
1. Merge to `main`
2. Create release tag
3. Deploy to staging
4. Verify functionality
5. Deploy to production

### Requirements
- All tests passing
- Security checks passed
- Performance benchmarks met
- Documentation updated

## Maintenance

### Regular Tasks
- Update dependencies
- Clean up old branches
- Archive old releases
- Update documentation

### Best Practices
- Keep branches up to date
- Regular security updates
- Monitor performance
- Maintain backups 