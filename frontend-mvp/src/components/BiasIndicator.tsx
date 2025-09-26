import React from 'react';
import { getBiasColor, getBiasLabel } from '../utils/bias';

interface BiasIndicatorProps {
  bias?: string;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
}

export const BiasIndicator: React.FC<BiasIndicatorProps> = ({
  bias,
  size = 'md',
  showLabel = true,
}) => {
  const color = getBiasColor(bias);
  const label = getBiasLabel(bias);

  const sizeClasses = {
    sm: 'w-2 h-2',
    md: 'w-3 h-3',
    lg: 'w-4 h-4',
  };

  const textSizeClasses = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base',
  };

  return (
    <div className="flex items-center gap-2">
      <div
        className={`${sizeClasses[size]} rounded-full`}
        style={{ backgroundColor: color }}
      />
      {showLabel && (
        <span className={`${textSizeClasses[size]} font-medium`} style={{ color }}>
          {label}
        </span>
      )}
    </div>
  );
};