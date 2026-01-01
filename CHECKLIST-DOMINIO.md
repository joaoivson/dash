# ✅ Checklist - Atualização de Domínio para marketdash.com.br

## 📝 Arquivos Atualizados

Todos os arquivos do backend foram atualizados com o novo domínio:

✅ **app/core/config.py** - CORS_ORIGINS atualizado
✅ **README-DEPLOY.md** - Documentação de deploy atualizada  
✅ **etapas.md** - Guia completo atualizado
✅ **README.md** - Documentação atualizada

---

## 🔧 Configurações no Supabase

Você precisa atualizar no Supabase Dashboard:

### 1. Produção (dashads-prod)

Acesse: https://supabase.com/dashboard/project/rsejwvxealraianensoz

**Authentication → Settings:**
- **Site URL**: `https://app.marketdash.com.br`
- **Redirect URLs**: Adicione/atualize:
  ```
  https://app.marketdash.com.br/**
  https://app-staging.marketdash.com.br/**
  http://localhost:3000/**
  http://localhost:5173/**
  http://localhost:8080/**
  ```

### 2. Staging (se tiver projeto separado)

Mesmas configurações acima, mas no projeto de staging.

---

## 🌐 Domínios Finais

### Produção:
- **Frontend**: `https://app.marketdash.com.br`
- **Backend API**: `https://api.marketdash.com.br`
- **Documentação**: `https://api.marketdash.com.br/docs`

### Staging/Homologação:
- **Frontend**: `https://app-staging.marketdash.com.br`
- **Backend API**: `https://api-staging.marketdash.com.br`
- **Documentação**: `https://api-staging.marketdash.com.br/docs`

---

## 🔐 Configuração de DNS

No painel da Hostinger, configure os registros A:

```
Tipo: A
Nome: api
Valor: [IP_DA_VPS]
TTL: 3600

Tipo: A
Nome: app
Valor: [IP_DA_VPS]
TTL: 3600

Tipo: A
Nome: api-staging
Valor: [IP_DA_VPS]
TTL: 3600

Tipo: A
Nome: app-staging
Valor: [IP_DA_VPS]
TTL: 3600
```

---

## ✅ Verificação

Após atualizar tudo, verifique:

```bash
# Backend Produção
curl https://api.marketdash.com.br/health

# Backend Staging
curl https://api-staging.marketdash.com.br/health

# Frontend Produção
curl https://app.marketdash.com.br

# Frontend Staging  
curl https://app-staging.marketdash.com.br
```

---

## 📋 Checklist Completo

- [x] Arquivos do backend atualizados
- [ ] Site URL atualizado no Supabase
- [ ] Redirect URLs atualizados no Supabase
- [ ] DNS configurado na Hostinger
- [ ] Domínios configurados no Coolify
- [ ] SSL gerado automaticamente
- [ ] Testes de acesso funcionando

---

**Status**: ✅ Backend atualizado, aguardando configurações no Supabase e DNS!

