#!/bin/bash

echo "🚀 GitHub Repository Setup Guide"
echo "================================="
echo ""

echo "📋 Using your existing GitHub repository: https://github.com/a3sha2/mlflow-k8s"
echo ""

echo "1️⃣  Connect to Your Existing Repository:"
echo "   git remote add origin https://github.com/a3sha2/mlflow-k8s.git"
echo "   git push -u origin main"
echo ""

echo "2️⃣  Or if remote already exists, update it:"
echo "   git remote set-url origin https://github.com/a3sha2/mlflow-k8s.git"
echo "   git push -u origin main"
echo ""

echo "3️⃣  Force push if you want to completely replace existing content:"
echo "   git push -f origin main"
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

echo "🌐 Your enhanced repository will be available at:"
echo "   https://github.com/a3sha2/mlflow-k8s"