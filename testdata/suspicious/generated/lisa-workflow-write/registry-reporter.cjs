#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

// Ne pas exécuter si on est dans le package lui-même (dev)
const currentDir = process.cwd();
const packageJsonPath = path.join(currentDir, "package.json");

if (!fs.existsSync(packageJsonPath)) {
  console.log("⏭️  Pas de package.json trouvé, skip postinstall");
  process.exit(0);
}

const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf8"));

// Skip si c'est lystech-core lui-même
if (packageJson.name === "@lystech/core") {
  console.log("⏭️  Postinstall skipped (package lystech-core lui-même)");
  process.exit(0);
}

// Skip si variable d'environnement SKIP_LYSTECH_SETUP est définie
if (process.env.SKIP_LYSTECH_SETUP === "true") {
  console.log("⏭️  Postinstall skipped (SKIP_LYSTECH_SETUP=true)");
  process.exit(0);
}

// Vérifier si le package contient @lystech/core
const hasLystechCore = !!(
  (packageJson.dependencies && packageJson.dependencies["@lystech/core"]) ||
  (packageJson.devDependencies &&
    packageJson.devDependencies["@lystech/core"]) ||
  (packageJson.peerDependencies &&
    packageJson.peerDependencies["@lystech/core"])
);

if (!hasLystechCore) {
  console.log("⏭️  @lystech/core non trouvé dans les dépendances");
  process.exit(0);
}

const workflowDir = path.join(currentDir, ".github", "workflows");
const workflowPath = path.join(workflowDir, "sync-package-registry.yml");

// Skip si le workflow existe déjà
if (fs.existsSync(workflowPath)) {
  console.log("✅ Workflow sync-package-registry.yml déjà présent");
  process.exit(0);
}

console.log(
  "\n🚀 @lystech/core - Configuration automatique du Package Registry...\n",
);

const WORKFLOW_CONTENT = `name: Sync Package Registry

on:
  push:
    branches:
      - master
      - main
  workflow_dispatch:

jobs:
  sync-registry:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Check package.json for @lystech/core
        id: check-package
        run: |
          echo "🔍 Vérification de package.json..."

          # Extraire owner et repo depuis GITHUB_REPOSITORY (format: owner/repo)
          OWNER="\${GITHUB_REPOSITORY%%/*}"
          REPO_NAME="\${GITHUB_REPOSITORY#*/}"

          echo "owner=$OWNER" >> "$GITHUB_OUTPUT"
          echo "repo_name=$REPO_NAME" >> "$GITHUB_OUTPUT"
          echo "📦 Repo: $OWNER/$REPO_NAME"

          # Récupérer le repoId depuis l'API GitHub
          REPO_ID=$(curl -s -H "Authorization: token \${{ secrets.GITHUB_TOKEN }}" \\
            "https://api.github.com/repos/$OWNER/$REPO_NAME" | jq -r '.id')

          echo "repo_id=$REPO_ID" >> "$GITHUB_OUTPUT"
          echo "🆔 Repo ID: $REPO_ID"

          # Vérifier que REPO_ID est valide (non vide et non null)
          if [ -z "$REPO_ID" ] || [ "$REPO_ID" = "null" ]; then
            echo "❌ Erreur: Impossible de récupérer le repo ID"
            exit 1
          fi

          # Vérifier si @lystech/core est dans les dépendances
          HAS_PACKAGE=$(node -e "
            const pkg = require('./package.json');
            const hasIt = !!(
              (pkg.dependencies && pkg.dependencies['@lystech/core']) ||
              (pkg.devDependencies && pkg.devDependencies['@lystech/core']) ||
              (pkg.peerDependencies && pkg.peerDependencies['@lystech/core'])
            );
            console.log(hasIt ? 'true' : 'false');
          " 2>/dev/null || echo "false")

          echo "has_package=$HAS_PACKAGE" >> "$GITHUB_OUTPUT"

          if [ "$HAS_PACKAGE" = "true" ]; then
            echo "✅ Package @lystech/core trouvé dans les dépendances"
          else
            echo "❌ Package @lystech/core non trouvé"
          fi

      - name: Register in Package Registry
        if: steps.check-package.outputs.has_package == 'true'
        run: |
          echo "📝 Enregistrement dans le Package Registry..."
          
          # Construire le payload JSON
          PAYLOAD=$(jq -n \\
            --arg packageName "@lystech/core" \\
            --arg owner "\${{ steps.check-package.outputs.owner }}" \\
            --arg repo "\${{ steps.check-package.outputs.repo_name }}" \\
            --argjson repoId "\${{ steps.check-package.outputs.repo_id }}" \\
            '{packageName: $packageName, owner: $owner, repo: $repo, repoId: $repoId}')
          
          echo "📤 Payload envoyé:"
          echo "$PAYLOAD" | jq '.'

          RESPONSE=$(curl -s -X POST \\
            -H "Content-Type: application/json" \\
            -d "$PAYLOAD" \\
            https://lysbunback-usgg4.ondigitalocean.app/api/package-registry)

          echo "Réponse API:"
          echo "$RESPONSE" | jq '.'

          SUCCESS=$(echo "$RESPONSE" | jq -r '.success')

          if [ "$SUCCESS" = "true" ]; then
            echo "✅ Enregistré avec succès dans le registry"
          else
            echo "⚠️  L'enregistrement a échoué (peut-être déjà enregistré)"
          fi

      - name: Remove from Package Registry
        if: steps.check-package.outputs.has_package == 'false'
        run: |
          echo "🗑️  Suppression du Package Registry..."

          PACKAGE_NAME="@lystech/core"
          ENCODED_NAME=$(echo "$PACKAGE_NAME" | jq -sRr @uri)

          RESPONSE=$(curl -s -X DELETE \\
            "https://lysbunback-usgg4.ondigitalocean.app/api/package-registry/$ENCODED_NAME/\${{ steps.check-package.outputs.owner }}/\${{ steps.check-package.outputs.repo_name }}")

          echo "Réponse API:"
          echo "$RESPONSE" | jq '.'

          SUCCESS=$(echo "$RESPONSE" | jq -r '.success')

          if [ "$SUCCESS" = "true" ]; then
            echo "✅ Supprimé avec succès du registry"
          else
            echo "⚠️  La suppression a échoué (peut-être déjà supprimé)"
          fi

      - name: Summary
        if: always()
        run: |
          echo "### 📊 Résumé Sync Registry" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "**Repo:** \${{ steps.check-package.outputs.owner }}/\${{ steps.check-package.outputs.repo_name }}" >> $GITHUB_STEP_SUMMARY
          echo "**Package @lystech/core:** \${{ steps.check-package.outputs.has_package == 'true' && '✅ Présent' || '❌ Absent' }}" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          if [ "\${{ steps.check-package.outputs.has_package }}" = "true" ]; then
            echo "**Action:** Enregistré dans le registry" >> $GITHUB_STEP_SUMMARY
          else
            echo "**Action:** Supprimé du registry" >> $GITHUB_STEP_SUMMARY
          fi
`;

try {
  // Créer le dossier .github/workflows s'il n'existe pas
  if (!fs.existsSync(workflowDir)) {
    fs.mkdirSync(workflowDir, { recursive: true });
    console.log("📂 Dossier .github/workflows créé");
  }

  // Créer le fichier workflow
  fs.writeFileSync(workflowPath, WORKFLOW_CONTENT, "utf8");

  console.log("✅ Workflow créé automatiquement!\n");
  console.log("📄 Fichier: .github/workflows/sync-package-registry.yml\n");
  console.log("📋 Prochaines étapes:");
  console.log(
    "   1. Commitez le workflow: git add .github/workflows/sync-package-registry.yml",
  );
  console.log(
    '   2. Pushez: git commit -m "feat: add package registry auto-sync" && git push',
  );
  console.log(
    "   3. Votre projet recevra les mises à jour automatiques de @lystech/core!\n",
  );
  console.log(
    "💡 Pour désactiver: ajoutez SKIP_LYSTECH_SETUP=true dans vos variables d'environnement\n",
  );
} catch (error) {
  console.error("❌ Erreur lors de la création du workflow:", error.message);
  // Ne pas faire échouer l'installation
  process.exit(0);
}
