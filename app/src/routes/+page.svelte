<script lang="ts">
    import { supabase } from '$lib/supabaseClient'
    import * as z from 'zod'
    import { superForm } from 'sveltekit-superforms/client'
    import { Button } from '$lib/components/ui/button'
    import { Input } from '$lib/components/ui/input'
    import { Label } from '$lib/components/ui/label'
    import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card'
    import { Alert, AlertDescription } from '$lib/components/ui/alert'
    import type { PageData } from './$types';
  
    export let data: PageData

    const { form, errors, enhance } = superForm(data.form)
  
    async function handleLogin() {
      const { data, error } = await supabase.auth.signInWithPassword({
        email: $form.email,
        password: $form.password
      })
  
      if (error) {
        console.error('Error logging in:', error.message)
        return
      }
  
      // Redirect or handle successful login
      window.location.href = '/dashboard'
    }
  </script>
  
  <div class="flex min-h-screen items-center justify-center">
    <Card class="w-[350px]">
      <CardHeader>
        <CardTitle>Login</CardTitle>
        <CardDescription>Enter your credentials to access your account</CardDescription>
      </CardHeader>
      <CardContent>
        <form on:submit|preventDefault={handleLogin} class="space-y-4">
          <div class="space-y-2">
            <Label for="email">Email</Label>
            <Input 
              id="email"
              type="email" 
              bind:value={$form.email}
              placeholder="name@example.com"
            />
            {#if $errors.email}
              <Alert variant="destructive">
                <AlertDescription>{$errors.email}</AlertDescription>
              </Alert>
            {/if}
          </div>
  
          <div class="space-y-2">
            <Label for="password">Password</Label>
            <Input 
              id="password"
              type="password" 
              bind:value={$form.password}
              placeholder="Enter your password"
            />
            {#if $errors.password}
              <Alert variant="destructive">
                <AlertDescription>{$errors.password}</AlertDescription>
              </Alert>
            {/if}
          </div>
  
          <Button type="submit" class="w-full">Sign in</Button>
        </form>
      </CardContent>
    </Card>
  </div>