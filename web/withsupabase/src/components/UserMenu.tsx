import { useEffect, useState } from 'react';
import { User } from '@supabase/supabase-js';
import { supabase } from '../lib/supabase';

interface UserMenuProps {
  user: User;
  onLogout: () => void;
}

export default function UserMenu({ user, onLogout }: UserMenuProps) {
  const [isOpen, setIsOpen] = useState(false);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    onLogout();
  };

  return (
    <div className="user-menu">
      <button className="user-btn" onClick={() => setIsOpen(!isOpen)}>
        👤 {user.email?.split('@')[0]}
      </button>
      {isOpen && (
        <div className="dropdown">
          <button onClick={handleLogout}>Logout</button>
        </div>
      )}
    </div>
  );
}
