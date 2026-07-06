import { useEffect, useMemo, useState } from 'react';
import { User } from '@supabase/supabase-js';
import { supabase } from './lib/supabase';
import Auth from './components/Auth';
import UserMenu from './components/UserMenu';

type Product = {
  id: number;
  name: string;
  price: number;
  description: string;
  image_url: string;
};

export default function App() {
  const [user, setUser] = useState<User | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [cart, setCart] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const missingSupabaseConfig = !import.meta.env.VITE_SUPABASE_URL || !import.meta.env.VITE_SUPABASE_ANON_KEY;

  // Check if user is logged in on mount
  useEffect(() => {
    const checkUser = async () => {
      const { data } = await supabase.auth.getSession();
      setUser(data.session?.user ?? null);
    };

    checkUser();

    const { data } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => {
      data.subscription.unsubscribe();
    };
  }, []);

  useEffect(() => {
    const loadProducts = async () => {
      const { data, error } = await supabase.from('products').select('*').order('id');
      if (error) {
        setError(error.message);
      } else {
        setProducts((data as Product[]) ?? []);
      }
      setLoading(false);
    };

    if (user) {
      loadProducts();
    }
  }, [user]);

  const addToCart = (product: Product) => {
    setCart((prev) => [...prev, product]);
  };

  const total = useMemo(() => cart.reduce((sum, item) => sum + item.price, 0), [cart]);

  if (missingSupabaseConfig) {
    return (
      <div className="app-shell">
        <div className="auth-card">
          <h1>Configuration required</h1>
          <p>Set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY in your deployment environment.</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Auth onAuthChange={() => {}} />;
  }

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Supabase + Vite + React</p>
          <h1>NovaCart</h1>
          <p>Modern products, fast checkout, and a polished storefront.</p>
        </div>
        <div className="hero-actions">
          <div className="hero-card">
            <h2>Cart</h2>
            <p>{cart.length} item(s)</p>
            <strong>${total.toFixed(2)}</strong>
          </div>
          <UserMenu user={user} onLogout={() => setUser(null)} />
        </div>
      </header>

      <main>
        <section className="product-grid">
          {loading && <p>Loading products…</p>}
          {error && <p className="error">{error}</p>}
          {!loading && !error && products.length === 0 && <p>No products available yet.</p>}
          {products.map((product) => (
            <article key={product.id} className="product-card">
              <img src={product.image_url} alt={product.name} />
              <div className="product-info">
                <h3>{product.name}</h3>
                <p>{product.description}</p>
                <div className="product-footer">
                  <span>${product.price.toFixed(2)}</span>
                  <button onClick={() => addToCart(product)}>Add to cart</button>
                </div>
              </div>
            </article>
          ))}
        </section>
      </main>
    </div>
  );
}
