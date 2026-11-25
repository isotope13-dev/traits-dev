---
---

# Sicherheit & DSGVO - Atoll Tourisme

## Überblick

**Sicherheit** und **DSGVO-Konformität** sind **OBLIGATORISCH** und kritisch für Atoll Tourisme.

**Ziele:**

> **DSGVO-Erinnerung:**
> Medizinische Daten (Allergien, Behandlungen) der Teilnehmer sind **sensible Daten**,
> die **Verschlüsselung** und **verstärkte Schutzmaßnahmen** erfordern.

> **Referenzen:**
> - `03-coding-standards.md` - Eingabevalidierung
> - `01-symfony-best-practices.md` - Symfony Security

---

## Inhaltsverzeichnis

1. [OWASP Top 10 Schutzmaßnahmen](#owasp-top-10-schutzmaßnahmen)
2. [DSGVO-Konformität](#dsgvo-konformität)
3. [Verschlüsselung sensibler Daten](#verschlüsselung-sensibler-daten)
4. [Validierung und Sanitization](#validierung-und-sanitization)
5. [Sicherheits-Header](#sicherheits-header)
6. [Audit Trail](#audit-trail)
7. [Sicherheits-Checkliste](#sicherheits-checkliste)

---

## OWASP Top 10 Schutzmaßnahmen

### 1. Injection (SQL, XSS, Command)

#### SQL-Injection

```php
<?php

// ❌ GEFÄHRLICH: SQL-Konkatenation
$sql = "SELECT * FROM reservation WHERE email = '" . $_POST['email'] . "'";
$result = $connection->query($sql);

$query = $entityManager->createQuery(
    'SELECT r FROM App\Entity\Reservation r WHERE r.email = :email'
);
$result = $query->getResult();

final class DoctrineReservationRepository
{
    public function findByEmail(Email $email): array
    {
        return $this->createQueryBuilder('r')
            ->where('r.email = :email')
            ->getQuery()
            ->getResult();
    }
}
```

#### XSS (Cross-Site Scripting)

```twig
{# ❌ GEFÄHRLICH: Rohe Ausgabe #}
{{ userInput|raw }}
<div>{{ comment|raw }}</div>

{{ userInput }}
<div>{{ comment }}</div>

{{ userInput|escape('html') }}
{{ userInput|e }}
```

```php
<?php

// ❌ GEFÄHRLICH: Direktes echo
echo $_POST['name'];

echo htmlspecialchars($_POST['name'], ENT_QUOTES, 'UTF-8');

return $this->render('reservation/show.html.twig', [
    'name' => $name, // Auto-escaped von Twig
]);
```

#### Command-Injection

```php
<?php

// ❌ GEFÄHRLICH: shell_exec mit Benutzereingabe
shell_exec('convert ' . $_POST['filename'] . ' output.pdf');

use Symfony\Component\Process\Process;

$process = new Process([
    'convert',
    'output.pdf',
]);
