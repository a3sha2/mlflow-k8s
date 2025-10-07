#!/bin/bash

echo "🚀 GitHub Repository Setup Guide"
echo "================================="
echo ""

echo "📋 Steps to create your private GitHub repository:"
echo ""

echo "1️⃣  Create Repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: mlflow-k8s-registry"
echo "   - Description: Production-ready MLflow Model Registry on Kubernetes with REST API and PostgreSQL backend"
echo "   - ✅ Private repository"
echo "   - ✅ Add README file: NO (we have our own)"
echo "   - ✅ Add .gitignore: NO (we have our own)"
echo "   - ✅ Choose a license: NO (we have MIT license)"
echo ""

echo "2️⃣  Connect Local Repository:"
echo "   Copy these commands and run them:"
echo ""
echo "   git remote add origin https://github.com/a3sha2/mlflow-k8s-registry.git"
echo "   git push -u origin main"
echo ""

echo "3️⃣  Alternative: Use GitHub CLI (if installed):"
echo "   gh repo create mlflow-k8s-registry --private --source=. --push"
echo ""

echo "📊 Repository Statistics:"
echo "   📁 Files: $(find . -type f | wc -l)"
echo "   📝 Scripts: $(find scripts/ -name '*.py' -o -name '*.sh' | wc -l)"
echo "   🐳 Kubernetes Manifests: $(find manifests/ -name '*.yaml' | wc -l)"
echo "   📋 Documentation: README.md, LICENSE, .gitignore"
echo ""

echo "🔍 Repository Structure:"
tree -a -I '.git' . 2>/dev/null || ls -la

echo ""
echo "✅ Ready to push! Your repository includes:"
echo "   🎯 Complete MLflow Kubernetes deployment"
echo "   🛠️  Management and demo scripts"
echo "   📚 Comprehensive documentation"
echo "   🔧 Configuration files"
echo "   📄 MIT License"
echo "   🚫 Proper .gitignore"
echo ""

echo "🌐 After pushing, your repo will be available at:"
echo "   https://github.com/a3sha2/mlflow-k8s-registry"